"""
https://github.com/Return-Log/BeepMusic
GPL-3.0 license
coding: UTF-8
"""

import mido
from mido import MidiFile
import winsound


def check_and_merge_tracks(midi_file):
    """
    检查MIDI文件是否为单轨道，如果不是，则合并所有轨道为一个轨道。

    :param midi_file: mido.MidiFile 对象
    :return: 合并后的单个轨道
    """
    if len(midi_file.tracks) == 1:
        return midi_file.tracks[0]
    else:
        merged_track = mido.MidiTrack()
        for track in midi_file.tracks:
            for msg in track:
                merged_track.append(msg)
        return merged_track


def get_notes_and_durations(track):
    """
    从轨道中提取音符和持续时间。

    :param track: mido.MidiTrack 对象
    :return: 包含音符和持续时间的列表，格式为[(note, duration), ...]
    """
    notes = []
    current_time = 0
    ongoing_notes = {}

    for msg in track:
        current_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            ongoing_notes[msg.note] = current_time
            current_time = 0
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in ongoing_notes:
                start_time = ongoing_notes.pop(msg.note)
                notes.append((msg.note, start_time + current_time))
                current_time = 0

    return notes


def play_notes(notes, speed_factor=1.0):
    """
    使用winsound函数播放音符和持续时间，并调整整体播放速度。

    :param notes: 包含音符和持续时间的列表
    :param speed_factor: 速度因子，用于调整播放速度。1.0表示原始速度，0.5表示减慢一半速度，2.0表示加快一倍速度。
    """
    for note, duration in notes:
        adjusted_duration = int(duration / speed_factor)
        print(f"note: {note}, duration: {adjusted_duration}")
        winsound.Beep(note_to_freq(note), adjusted_duration)


def note_to_freq(note):
    """
    将MIDI音符转换为频率。

    :param note: MIDI音符编号
    :return: 对应的频率
    """
    A4 = 440
    return int(A4 * 2 ** ((note - 69) / 12))


def process_midi(file_path, speed_factor=1.0):
    """
    处理MIDI文件：读取文件，检查或合并轨道，提取音符和持续时间，播放音符。

    :param file_path: MIDI文件路径
    :param speed_factor: 速度因子，用于调整播放速度。
    """
    midi_file = MidiFile(file_path)
    track = check_and_merge_tracks(midi_file)
    notes = get_notes_and_durations(track)
    play_notes(notes, speed_factor)


# 播放
file_path = '亲爱的父亲片段.mid'  # MIDI文件路径
speed_factor = 0.5  # 调整播放速度
process_midi(file_path, speed_factor)
