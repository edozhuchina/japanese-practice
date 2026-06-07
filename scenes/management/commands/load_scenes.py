from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = '加载初始日语学习场景数据'

    def handle(self, *args, **options):
        self.stdout.write('正在加载场景数据...')
        try:
            call_command('loaddata', 'initial_scenes', verbosity=1)
            self.stdout.write(self.style.SUCCESS('场景数据加载成功！'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'加载失败: {e}'))
            self.stdout.write('如果数据已存在，请尝试先清除:')
            self.stdout.write('  python manage.py flush --no-input')
