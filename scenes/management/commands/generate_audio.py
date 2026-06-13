"""
使用 Edge TTS 为所有对话生成日语语音文件
用法: python manage.py generate_audio [--force] [--voice ja-JP-NanamiNeural]
"""
import os
import asyncio
import edge_tts
from django.core.management.base import BaseCommand
from scenes.models import Dialogue


class Command(BaseCommand):
    help = '使用 Edge TTS 为所有对话生成日语 mp3 语音文件'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='强制重新生成所有音频（即使已存在）'
        )
        parser.add_argument(
            '--voice', type=str, default='ja-JP-NanamiNeural',
            help='TTS 语音名称 (默认: ja-JP-NanamiNeural)'
        )
        parser.add_argument(
            '--rate', type=str, default='-10%',
            help='语速调整 (默认: -10%% 稍慢)'
        )

    def handle(self, *args, **options):
        force = options['force']
        voice = options['voice']
        rate = options['rate']

        # 音频输出目录：frontend/audio/
        audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))),
            'frontend', 'audio'
        )
        os.makedirs(audio_dir, exist_ok=True)

        dialogues = Dialogue.objects.all().order_by('id')
        total = dialogues.count()
        self.stdout.write(f'共 {total} 条对话需要处理')
        self.stdout.write(f'语音: {voice} | 语速: {rate}')
        self.stdout.write(f'输出目录: {audio_dir}\n')

        generated = 0
        skipped = 0
        errors = 0

        for d in dialogues:
            filename = f'dialogue_{d.id}.mp3'
            filepath = os.path.join(audio_dir, filename)

            if os.path.exists(filepath) and not force:
                skipped += 1
                self.stdout.write(f'  ⏭  [{d.id:2d}/{total}] 已存在: {filename}')
                # 更新数据库 audio_url
                audio_url = f'audio/{filename}'
                if d.audio_url != audio_url:
                    d.audio_url = audio_url
                    d.save(update_fields=['audio_url'])
                continue

            try:
                self.stdout.write(f'  🎙  [{d.id:2d}/{total}] 生成中: {d.japanese_text[:30]}...')
                asyncio.run(self._generate(d.japanese_text, filepath, voice, rate))

                # 更新数据库
                audio_url = f'audio/{filename}'
                d.audio_url = audio_url
                d.save(update_fields=['audio_url'])

                generated += 1
                size_kb = os.path.getsize(filepath) / 1024
                self.stdout.write(f'  ✅ 完成 ({size_kb:.1f} KB)')
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f'  ❌ 失败: {e}'))

        self.stdout.write(f'\n{"="*50}')
        self.stdout.write(self.style.SUCCESS(
            f'完成！生成: {generated} | 跳过: {skipped} | 失败: {errors}'
        ))

    async def _generate(self, text, filepath, voice, rate):
        """异步生成单个音频文件"""
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(filepath)
