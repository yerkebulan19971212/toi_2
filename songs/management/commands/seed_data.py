"""
Management command to seed example data for development.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed the database with example data'

    def handle(self, *args, **options):
        self._seed_song_categories()
        self._seed_songs()
        self._seed_invitation_templates()
        self._seed_blog_posts()
        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))

    def _seed_song_categories(self):
        from songs.models import SongCategory
        categories = [
            {'name': 'Дәстүрлі той әндері', 'slug': 'daстурли', 'order': 1},
            {'name': 'Жар жар', 'slug': 'zhar-zhar', 'order': 2},
            {'name': 'Беташар', 'slug': 'betashar', 'order': 3},
            {'name': 'Заманауи той', 'slug': 'zamanauy', 'order': 4},
        ]
        for cat in categories:
            SongCategory.objects.get_or_create(slug=cat['slug'], defaults=cat)
        self.stdout.write('  Song categories created.')

    def _seed_songs(self):
        from songs.models import Song, SongCategory
        try:
            default_cat = SongCategory.objects.first()
        except SongCategory.DoesNotExist:
            default_cat = None

        songs = [
            {'title': 'Жар жар', 'artist': 'Халық әні', 'duration': 185, 'order': 1},
            {'title': 'Беташар', 'artist': 'Халық әні', 'duration': 210, 'order': 2},
            {'title': 'Құдаша', 'artist': 'Халық әні', 'duration': 195, 'order': 3},
            {'title': 'Шашу', 'artist': 'Халық әні', 'duration': 160, 'order': 4},
            {'title': 'Той бастар', 'artist': 'Халық әні', 'duration': 240, 'order': 5},
            {'title': 'Келін түсіру', 'artist': 'Халық әні', 'duration': 220, 'order': 6},
            {'title': 'Думан той', 'artist': 'Халық әні', 'duration': 175, 'order': 7},
            {'title': 'Той думан', 'artist': 'Халық әні', 'duration': 190, 'order': 8},
            {'title': 'Қыз ұзату', 'artist': 'Халық әні', 'duration': 230, 'order': 9},
            {'title': 'Сыңсу', 'artist': 'Халық әні', 'duration': 200, 'order': 10},
            {'title': 'Жеңге той', 'artist': 'Халық әні', 'duration': 165, 'order': 11},
            {'title': 'Бесік жыры', 'artist': 'Халық әні', 'duration': 180, 'order': 12},
        ]
        for song_data in songs:
            song_data['category'] = default_cat
            Song.objects.get_or_create(
                title=song_data['title'],
                artist=song_data['artist'],
                defaults=song_data
            )
        self.stdout.write('  Songs created.')

    def _seed_invitation_templates(self):
        from invitations.models import InvitationTemplate
        templates = [
            {
                'name': 'PRESTIGE',
                'category': 'uzatu',
                'gradient_from': '#C9A84C',
                'gradient_to': '#8B6914',
                'price': 2500,
                'is_featured': True,
            },
            {
                'name': 'DARАБОЗА',
                'category': 'sunnet',
                'gradient_from': '#2D5016',
                'gradient_to': '#1A3009',
                'price': 3000,
                'is_featured': True,
            },
            {
                'name': 'MIRELA',
                'category': 'qyz_uzatu',
                'gradient_from': '#7B3F00',
                'gradient_to': '#4A2500',
                'price': 3500,
                'is_featured': True,
            },
            {
                'name': 'Алтын той',
                'category': 'merey',
                'gradient_from': '#F6C15C',
                'gradient_to': '#E8963C',
                'price': 2000,
                'is_featured': False,
            },
            {
                'name': 'Жасыл бақ',
                'category': 'besik',
                'gradient_from': '#40B49A',
                'gradient_to': '#0D7B6A',
                'price': 1500,
                'is_featured': False,
            },
            {
                'name': 'Аспан',
                'category': 'betashar',
                'gradient_from': '#667EEA',
                'gradient_to': '#764BA2',
                'price': 2000,
                'is_featured': False,
            },
            {
                'name': 'Бесік',
                'category': 'tusaukesar',
                'gradient_from': '#F97316',
                'gradient_to': '#EF4444',
                'price': 1500,
                'is_free': True,
                'is_featured': False,
            },
            {
                'name': 'Арман',
                'category': 'other',
                'gradient_from': '#9333EA',
                'gradient_to': '#EC4899',
                'price': 0,
                'is_free': True,
                'is_featured': False,
            },
        ]
        for t in templates:
            InvitationTemplate.objects.get_or_create(name=t['name'], defaults=t)
        self.stdout.write('  Invitation templates created.')

    def _seed_blog_posts(self):
        from blog.models import BlogPost
        posts = [
            {
                'title': 'Үйлену тойына арналған ең үздік тілектер',
                'slug': 'top-wedding-wishes',
                'excerpt': 'Тойыңызды ерекше ету үшін ең жылы тілектер жинағы.',
                'content': 'Той — өмірдегі ең маңызды оқиғалардың бірі. Жақындарыңызға жылы тілек айту арқылы олардың қуанышына ортақ болыңыз.',
                'is_published': True,
                'published_at': timezone.now(),
            },
            {
                'title': 'Үйлену тойында дәстүрлі ойындарды қалай ұйымдастыруға болады?',
                'slug': 'traditional-wedding-games',
                'excerpt': 'Қазақ тойының дәстүрлі ойындары мен оларды ұйымдастыру кеңестері.',
                'content': 'Қазақ тойы — жанды және қызықты мерекелердің бірі. Жар жар, беташар және басқа да дәстүрлі ойындар тойыңызды ерекше етеді.',
                'is_published': True,
                'published_at': timezone.now(),
            },
            {
                'title': 'Той шақыруын қалай дайындауға болады? 5 қарапайым қадам',
                'slug': 'how-to-make-invitation',
                'excerpt': 'Shaqyru.kz арқылы 5 минутта кәсіби той шақыруын жасаңыз.',
                'content': 'Той шақыруын жасау енді оңай! Платформамызды пайдаланып, өзіңіздің ерекше шақыруыңызды жасаңыз.',
                'is_published': True,
                'published_at': timezone.now(),
            },
        ]
        for post in posts:
            BlogPost.objects.get_or_create(slug=post['slug'], defaults=post)
        self.stdout.write('  Blog posts created.')
