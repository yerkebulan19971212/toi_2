from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Guest,
    GuestComment,
    Invitation,
    InvitationCategory,
    InvitationTemplate,
    RSVPResponse,
)
from .serializers import (
    GuestCommentSerializer,
    GuestSerializer,
    InvitationCategorySerializer,
    InvitationReadSerializer,
    InvitationTemplateSerializer,
    InvitationWriteSerializer,
    RSVPResponseSerializer,
    RSVPResultsSerializer,
)


# ---------------------------------------------------------------------------
# Categories & Templates
# ---------------------------------------------------------------------------

class CategoryListView(generics.ListAPIView):
    queryset = InvitationCategory.objects.filter(is_active=True)
    serializer_class = InvitationCategorySerializer


class TemplateListView(generics.ListAPIView):
    queryset = InvitationTemplate.objects.filter(is_active=True)
    serializer_class = InvitationTemplateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=int(category))
            else:
                qs = qs.filter(category__code=category)
        return qs


class TemplateDetailView(generics.RetrieveAPIView):
    queryset = InvitationTemplate.objects.filter(is_active=True)
    serializer_class = InvitationTemplateSerializer


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------

class InvitationCreateView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        # Return full read representation after creation
        read_serializer = InvitationReadSerializer(
            invitation, context={'request': request}
        )
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class InvitationDetailView(generics.RetrieveUpdateAPIView):
    queryset = Invitation.objects.prefetch_related('images', 'guests').all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return InvitationWriteSerializer
        return InvitationReadSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True  # always allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        read_serializer = InvitationReadSerializer(
            invitation, context={'request': request}
        )
        return Response(read_serializer.data)


# ---------------------------------------------------------------------------
# Guest list management (existing feature)
# ---------------------------------------------------------------------------

class GuestCreateView(generics.CreateAPIView):
    serializer_class = GuestSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)


# ---------------------------------------------------------------------------
# Guest Comments
# ---------------------------------------------------------------------------

class GuestCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = GuestCommentSerializer

    def get_queryset(self):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        return GuestComment.objects.filter(
            invitation=invitation, is_approved=True
        )

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)


# ---------------------------------------------------------------------------
# RSVP
# ---------------------------------------------------------------------------

class RSVPCreateView(generics.CreateAPIView):
    serializer_class = RSVPResponseSerializer

    def perform_create(self, serializer):
        invitation = get_object_or_404(Invitation, slug=self.kwargs['slug'])
        serializer.save(invitation=invitation)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception:
            # unique_together violation — phone already responded
            return Response(
                {'detail': 'Сіз бұрын жауап бергенсіз.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RSVPResultsView(APIView):
    """Aggregated RSVP counts for an invitation."""

    def get(self, request, slug):
        invitation = get_object_or_404(Invitation, slug=slug)
        counts = (
            invitation.rsvp_responses
            .values('response')
            .annotate(count=Count('id'))
        )
        result = {row['response']: row['count'] for row in counts}
        data = {
            'solo':         result.get('solo', 0),
            'with_partner': result.get('with_partner', 0),
            'declined':     result.get('declined', 0),
            'total_guests': result.get('solo', 0) + result.get('with_partner', 0) * 2,
        }
        return Response(RSVPResultsSerializer(data).data)


# ---------------------------------------------------------------------------
# Public invitation HTML page
# ---------------------------------------------------------------------------

_RSVP_SNIPPET = """
<style>
#rsvp-box{max-width:480px;margin:2rem auto;padding:1.5rem;font-family:sans-serif}
#rsvp-box h3{text-align:center;margin-bottom:1rem;font-size:1.1rem}
#rsvp-box input{width:100%;padding:.6rem .8rem;margin-bottom:.6rem;border:1px solid #ccc;border-radius:8px;font-size:.95rem;box-sizing:border-box}
.rsvp-btns{display:flex;flex-direction:column;gap:.5rem}
.rsvp-btn{padding:.8rem;border:none;border-radius:10px;font-size:.95rem;cursor:pointer;font-weight:600;transition:.15s}
.rsvp-btn:disabled{opacity:.5}
.btn-yes{background:#22c55e;color:#fff}
.btn-pair{background:#3b82f6;color:#fff}
.btn-no{background:#e5e7eb;color:#374151}
#rsvp-msg{margin-top:.8rem;text-align:center;font-size:.9rem;padding:.5rem;border-radius:8px}
.msg-ok{background:#dcfce7;color:#166534}
.msg-err{background:#fee2e2;color:#991b1b}
</style>
<div id="rsvp-box">
  <h3>Қатысуыңызды растаңыз</h3>
  <input id="rsvp-name" placeholder="Аты-жөні" />
  <input id="rsvp-phone" placeholder="Телефон (міндетті емес)" />
  <div class="rsvp-btns">
    <button class="rsvp-btn btn-yes" onclick="submitRsvp('solo')">Иә, жалғыз өзім барамын</button>
    <button class="rsvp-btn btn-pair" onclick="submitRsvp('with_partner')">Жұбайыммен бірге барамын</button>
    <button class="rsvp-btn btn-no" onclick="submitRsvp('declined')">Өкінішке орай, келе алмаймын</button>
  </div>
  <div id="rsvp-msg" style="display:none"></div>
</div>
<script>
function submitRsvp(choice){
  var name=document.getElementById('rsvp-name').value.trim();
  if(!name){alert('Аты-жөні міндетті');return;}
  var phone=document.getElementById('rsvp-phone').value.trim();
  var slug=location.pathname.replace(/^\\/i\\/|\\/$/g,'');
  document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=true});
  fetch('/api/invitations/'+slug+'/rsvp/',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({guest_name:name,phone:phone,response:choice})
  }).then(function(r){
    var msg=document.getElementById('rsvp-msg');
    msg.style.display='block';
    if(r.ok||r.status===409){
      msg.className='msg-ok';
      msg.textContent=r.status===409?'Сіз бұрын жауап бергенсіз.':'Жауабыңыз қабылданды! Рахмет!';
      document.getElementById('rsvp-box').querySelector('h3').style.display='none';
      document.getElementById('rsvp-name').style.display='none';
      document.getElementById('rsvp-phone').style.display='none';
      document.querySelector('.rsvp-btns').style.display='none';
    }else{
      msg.className='msg-err';
      msg.textContent='Қате кетті. Кейінірек қайталаңыз.';
      document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=false});
    }
  }).catch(function(){
    var msg=document.getElementById('rsvp-msg');
    msg.style.display='block';msg.className='msg-err';
    msg.textContent='Желі қатесі. Кейінірек қайталаңыз.';
    document.querySelectorAll('.rsvp-btn').forEach(function(b){b.disabled=false});
  });
}
</script>
"""


class InvitationHTMLView(APIView):
    """Render invitation HTML page with RSVP form."""
    permission_classes = []

    def get(self, request, slug):
        from .renderer import render_invitation
        invitation = get_object_or_404(Invitation, slug=slug)

        if invitation.template and invitation.template.html_template:
            ctx = invitation.get_render_context()
            try:
                html = render_invitation(invitation.template.html_template, ctx)
            except Exception:
                html = invitation.rendered_html or ''
        else:
            html = invitation.rendered_html or ''

        if not html:
            html = '<html><body style="font-family:sans-serif;text-align:center;padding:3rem"><p>Шаблон жоқ</p></body></html>'

        # Inject RSVP form before </body>
        if '</body>' in html:
            html = html.replace('</body>', _RSVP_SNIPPET + '</body>', 1)
        else:
            html += _RSVP_SNIPPET

        return HttpResponse(html, content_type='text/html; charset=utf-8')
