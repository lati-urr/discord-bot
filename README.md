# discord-bot(rewrite)

**Discordのbotって？**
**何が出来るの？**
**試してみた！**

ローカルのmp3をボイチャで流したいなって作ったやつ．
効果音みたいなのを流したくて，いわゆる，music-botだと，特定の時間帯だけ抽出して流すみたいなことが出来なかったので，とりあえず，ローカルの曲を流す方針で．
多分やらないだろうけど，youtubeの時間指定してサビだけ抽出して流すbotほしいな．

**rewrite版です**

## 環境
- python 3.8.3
- pip 20.3.3
- discord 1.0.1

## install
```
git clone git@github.com:lati-urr/discord-bot.git
cd discord-bot
pip install requirements.txt
```
環境変数設定(.bash_profileに書くなり，実行するなり)
```
export DISCORD_TOKEN='トークン値'
export VOICECHAT_ID=ボイチャのID
```

## setting
コマンドと対応する音楽
dictionary.pyを開いて
```
dict = {'?ziman' : 'スネ夫の自慢話.mp3',
        '?ganbare' : '負けないで.mp3',
      }
```
mp3は，discord-bot以下(bot.pyとかdictionary.pyとかと同じディレクトリに配置)

## usage
```
python bot.py
```

**いかがでしたか？**
