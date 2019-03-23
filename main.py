import discord
import sys
from io import StringIO
import contextlib
import pip
import urllib.request
import os
import runpy
import json


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

TOKEN = json.loads(open('credentials.json').read())['token']

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    code = None
    if message.content.startswith('!python'):
        code = ' '.join(message.content.split(' ')[1:])
        with stdoutIO() as s:
            try:
                exec(code)
            except Exception as e:
                print(e)
            if len(s.getvalue()) < 1500:
                _message = s.getvalue()
            else :
                _message = s.getvalue()
                _message = message[:500] + "\n ... \n" + message[-500:]

        import ipdb; ipdb.set_trace()
        await client.send_message(message.channel, "Output is ```%s```" % _message)
    elif message.attachments:
        for attachement in message.attachments:
            if attachement['filename'].endswith('.py'):
                print(attachement['url'])
                user_agent = {'User-agent': 'Mozilla/5.0'}
                req = urllib.request.Request(
                    attachement['url'], 
                    data=None, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
                )
                response = urllib.request.urlopen(req)
                content = response.read()
                with open("somefile.py", "w+") as f:
                    f.write(content.decode('utf-8').replace('plt.show()', 'plt.savefig("fig.png")'))
                with stdoutIO() as s:
                    try:
                        out = runpy.run_path('./somefile.py')
                    except Exception as e:
                        print(e)
                if os.path.exists('./fig.png'):
                        await client.send_file(message.channel, 'fig.png')
                        os.remove('fig.png')
                if len(s.getvalue()) < 1500:
                    _message = s.getvalue()
                else :
                    _message = s.getvalue()
                    _message = message[:500] + "\n ... \n" + message[-500:]

                import ipdb; ipdb.set_trace()
                await client.send_message(message.channel, "Output is ```%s```" % _message)
                    

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
