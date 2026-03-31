from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os
import numpy as np


def montar_video_final(frames, durations, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    audio_path = "assets/sounds/discord-notification.mp3"
    clips = []

    # Verifica se o arquivo de áudio existe
    notif_audio = None
    if os.path.exists(audio_path):
        notif_audio = AudioFileClip(audio_path)
    else:
        print(f"⚠️ Áudio não encontrado em '{audio_path}'. O vídeo ficará sem som.")

    for i, frame in enumerate(frames):
        # Converte o frame PIL para array numpy que o MoviePy entende
        img_array = np.array(frame)
        duration = durations[i] if i < len(durations) else 2.0

        # Cria um mini clipe de vídeo para este frame específico
        clip = ImageClip(img_array).set_duration(duration)

        # Se o áudio existir, adiciona no início deste clipe
        if notif_audio:
            # Corta o áudio para não passar da duração da mensagem (evita bugs)
            audio_duration = min(notif_audio.duration, duration)
            clip_audio = notif_audio.subclip(0, audio_duration)
            clip = clip.set_audio(clip_audio)

        clips.append(clip)

    # Junta todos os clipes individuais em ordem
    final_clip = concatenate_videoclips(clips, method="compose")

    # Renderiza o vídeo final
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",  # Necessário para processar o som corretamente
    )
