import discord
import random
import os
from keep import keep_alive
import datetime

# 自分のトークンに置き換えてください

# Intentsを設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の取得を許可

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # にゃーんコマンド
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    if message.content == '/command':
        await message.channel.send('/neko ねこ\n'
                                   '/weekplan_valo valo募集\n'
                                   '/raffle valo抽選')

    if message.content == '/weekplan_valo':
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        weekday_names = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

        # 最初に見出しメッセージを送る
        await message.channel.send("🎮 今週のVALO募集")

        # 各曜日の日付を1つずつ送信
        for i in range(7):
            day_date = start_of_week + datetime.timedelta(days=i)
            day_name = weekday_names[i]
            msg = f"📅 {day_name}: {day_date.strftime('%Y-%m-%d')}"
            await message.channel.send(msg)
    # 抽選コマンド
    elif message.content == '/raffle':
        role_pool = {
            "コントローラー": ["オーメン", "ブリムストーン", "ヴァイパー", "アストラ", "ハーバー", "クローヴ"],
            "デュエ":
            ["ジェット", "フェニックス", "レイナ", "ヨル", "ネオン", "アイソ", "ウェイレイ", "レイズ"],
            "センチ": ["セージ", "サイファー", "キルジョイ", "チェンバー", "デッドロック", "ヴァイス"],
            "イニシ": ["ブリーチ", "ソーヴァ", "スカイ", "KAY/O", "フェイド", "ゲッコー"],
        }

        # フレックスを除いた4ロールで抽選
        roles = ["コントローラー", "デュエ", "センチ", "イニシ"]
        random.shuffle(roles)

        used_characters = set()
        results = []

        for i in range(4):
            role = roles[i]
            candidates = [
                c for c in role_pool[role] if c not in used_characters
            ]
            if not candidates:
                await message.channel.send(f"{role}に使用可能なキャラがいません。")
                return
            character = random.choice(candidates)
            used_characters.add(character)
            results.append((i + 1, role, character))

        # フレックス枠：全キャラから未使用を選ぶ
        all_characters = set()
        for char_list in role_pool.values():
            all_characters.update(char_list)

        available_flex = list(all_characters - used_characters)
        if not available_flex:
            await message.channel.send("フレックスに使用可能なキャラがいません。")
            return
        flex_char = random.choice(available_flex)
        results.append((5, "フレックス", flex_char))

        # 結果メッセージを作成して送信
        result_text = "** 抽選結果 **\n"
        for index, role, char in results:
            result_text += f"{index}. {role}：{char}\n"

        await message.channel.send(result_text)


# Botの起動
server_thread()
client.run(TOKEN)

