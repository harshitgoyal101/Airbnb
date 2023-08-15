from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import telegram
import requests
import time

updater = Updater("6016657369:AAHBx-jIcMAG6jlE0UzSbCdoq92xFW4Wam4",
				use_context=True)
chat_id = "+kx6fC6TEYPA5YjFl"

def get_user_name(user):
	name = ""
	if user.first_name:
		name = user.first_name
	if user.last_name:
		name += user.last_name
	if user['username']:
		name = user['username']
	if name == "":
		raise Exception("")
	return name

def start(update: Update, context: CallbackContext):
	update.message.reply_text("""
Welcome! This bot lets you play Russian Roulette with your friends.
\n<b>BULLET</b> is required to play. Each player places a bet before the game starts. The revolver is loaded with a single bullet and passed around in a circle. Each player must pull the trigger at least once before passing the gun. Once a player shoots themself, the game ends and their wager is distributed proportionally amongst the survivors based on the size of their bet.
\nThe size of the revolver along with the minimum bet is decided at the start of each game.
\nFirst, /connect a wallet. You will need to call <b>connectAndApprove</b> on the token contract and enter the correct secret. This will also approve infinite spending of the betting token by the bot. DM the transaction hash to the bot, and it will check that you entered the correct secret to connect your wallet. Once connected, buy <b>BULLET</b> as needed and you are ready to play!
\nGame portal: https://t.me/BulletGameDarkPortal
\nTwitter: https://twitter.com/BulletGameERC
\nDocs: https://bullet-game.gitbook.io/bullet-game
\nBuy <b>BULLET</b> on Uniswap: https://app.uniswap.org/#/swap?outputCurrency=0x8ef32a03784c8Fd63bBf027251b9620865bD54B6&chain=ethereum
\<b>BULLET</b> Contract: 0x8ef32a03784c8Fd63bBf027251b9620865bD54B6
\nRoulette Contract: 0x4d2E8a0ebC4BB3BE7F3d65426F6a0C5836635DBE
\nLinked Wallet: None (please /connect)
\n<b>Commands</b>
/start - Print this message
/connect - Connect a wallet to your Telegram account
/roulette - Start a new game
/join - Join a game
/bet - Place a bet
/pull - Pull the trigger
/pass - Pass the gun
/stop - Vote to stop the game (all bets will be refunded)
/leaderboard - View leaders in various categories
/min_bid - <b>ADMIN ONLY</b> - Set the minimum bid for a Telegram grouop
/fix - <b>ADMIN ONLY</b> - Clear game state and revert game in progress
""",  parse_mode=telegram.ParseMode.HTML)
	

def link(update: Update, context: CallbackContext):
	user = update.message.from_user
	try:
		tgUserName = get_user_name(user)
	except Exception:
		update.message.reply_text("You need a username to connect to the game")
		return
	tgUserID = user.id
	user_input = update.message.text
	url = f"https://game.tradebotserver.xyz/bullet/api/connect/{tgUserName}/{tgUserID}/{user_input}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		update.message.reply_text("\nJoin the group - https://t.me/"+chat_id)
	else:
		update.message.reply_text(result.json().get("message"))


def connect(update: Update, context: CallbackContext):
	if update.effective_chat.id == -1001903038672:
		update.message.reply_text("Tag the following button to connect to this in DM", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Connect to chat', url='https://t.me/harshit_goyal_101_bot')]]),  parse_mode=telegram.ParseMode.HTML)
		return 
	user = update.message.from_user
	tgUserID = user.id
	update.message.reply_text("""
Use Etherscan and call <b>connectAndApprove</b> on <b>BULLET</b> with the following value:
			   
secret: """+str(tgUserID)+"""

Then paste <b>ONLY</b> the transaction hash in this chat, for example:
0x396137aef7e09d9946ca2a437ed025e59a3d3852b728f4dbd643e5c4675e681a
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Etherscan', url='https://testnet.bscscan.com/address/0x227b25375e42c74356c51a0e6ca94518d6b64207')]]),  parse_mode=telegram.ParseMode.HTML)
	updater.dispatcher.add_handler(MessageHandler(Filters.text, link))
	

def can_start_a_new_game():
	if chat_id == -1001903038672:
		return 
	url = "https://game.tradebotserver.xyz/bullet/api/game/isAbleToInitiateGame"
	result = requests.get(url)
	print(result.json())
	return result.json().get("data", {}).get("isAbleToInitiateGame", False)

def start_game():
	url = "https://game.tradebotserver.xyz/bullet/api/game/start"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		return result.json().get("data", {}).get("link", ""), True
	else:
		return result.json().get("message"), False

def get_player():
	url = "https://game.tradebotserver.xyz/bullet/api/game/inProgressGamePlayers"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		return result.json().get("data", {}).get("players", [])
	else:
		return []

def cancel_game():
	url = "https://game.tradebotserver.xyz/bullet/api/game/cancel"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		return "+1"
	else:
		return result.json().get("message", "")

def initiate_game(tgUserID, revolverSize, minBet):
	url = "https://game.tradebotserver.xyz/bullet/api/game/initiate"
	myobj = {
		"tgUserId": str(tgUserID),
		"tgChatId": "-1903038672",
		"revolverSize": revolverSize,
		"minBet": minBet
	}
	result = requests.post(url, json = myobj)
	print(result.json())
	if result.json().get("success", False):
		return "+1"
	else:
		return result.json().get("message", "")

def roulette(update: Update, context):
	if chat_id == -1001903038672:
		return 
	if can_start_a_new_game():
		user = update.message.from_user
		tgUserID = user.id
		try:
			revolverSize = int(context.args[0])
			minBet = int(context.args[1])
		except Exception:
			update.message.reply_text("Invalid input")
			return 
		game_iun = initiate_game(tgUserID, revolverSize, minBet)
		if game_iun == "+1":
			update.message.reply_text(f"{get_user_name(user)} is starting a game of Russian Roulette using a {revolverSize} shot revolver. The minimum bid is <b>{minBet} BULLET</b>. /join the game.", parse_mode=telegram.ParseMode.HTML)
		else:
			update.message.reply_text(game_iun)
			return
		update.message.reply_text("There are 15 seconds to join the game.")
		time.sleep(15)
		player = get_player()
		if len(player) > 1:
			update.message.reply_text(f"Joining is now closed. Please place your bet's. The minimum is {minBet} BULLET.")
			update.message.reply_text("There are 15 seconds to bet before the game starts.")	
			time.sleep(15)
			link, start = start_game()
			if not start:
				update.message.reply_text(link)
				update.message.reply_text("Cancelling Game, Not enough Players")
				cn = cancel_game()
				if cn == "+1":
					update.message.reply_text("Game cancelled.")
				else:
					update.message.reply_text(cn)
				return
			else:
				update.message.reply_text(f"Betting closed. Loading game...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Etherscan', url=link)]]), parse_mode=telegram.ParseMode.HTML)
		else:
			update.message.reply_text("Cancelling Game, Not enough Players")
			cn = cancel_game()
			if cn == "+1":
				update.message.reply_text("Game cancelled.")
			else:
				update.message.reply_text(cn)
	else: 
		update.message.reply_text("Game already started")


def flush(update: Update, context: CallbackContext):
	if chat_id == -1001903038672:
		return 
	url = "https://game.tradebotserver.xyz/bullet/api/user/flush"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		update.message.reply_text("Flushed.")
	else:
		update.message.reply_text(result.json().get("message", ""))


def join(update: Update, context: CallbackContext):
	if chat_id == -1001903038672:
		return 
	user = update.message.from_user
	tgUserID = user.id
	try:
		tgUserName = get_user_name(user)
	except Exception:
		update.message.reply_text("You need a username to join.")
		return
	url = f"https://game.tradebotserver.xyz/bullet/api/game/addPlayer/{tgUserID}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		update.message.reply_text(f"{tgUserName} has join'd the game.")
	else:
		update.message.reply_text(result.json().get("message", ""))


def bet(update: Update, context):
	if chat_id == -1001903038672:
		return 
	user = update.message.from_user
	try:
		betAmount = int(context.args[0])
	except Exception:
		update.message.reply_text("Invalid input")
		return 
	try:
		tgUserName = get_user_name(user)
	except Exception:
		update.message.reply_text("You need a username to bet")
		return
	tgUserID = user.id
	url = f"https://game.tradebotserver.xyz/bullet/api/game/bet/{tgUserID}/{betAmount}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		update.message.reply_text(f"{tgUserName} bet {betAmount}.")
	else:
		update.message.reply_text(result.json().get("message"))


def pull(update: Update, context: CallbackContext):
	if chat_id == -1001903038672:
		return 
	user = update.message.from_user
	tgUserID = user.id
	url = f"https://game.tradebotserver.xyz/bullet/api/game/pull/{tgUserID}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		if not result.json().get("data",{}).get("isShot", False):
			update.message.reply_text(result.json().get("data",{}).get("text"))
		else:
			link = result.json().get("data",{}).get("link", "")
			text = result.json().get("data",{}).get("link", "")
			update.message.reply_text(f"""
{text}
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Etherscan', url=link)]]), parse_mode=telegram.ParseMode.HTML)
	else:
		update.message.reply_text(result.json().get("message"))


def pass_text(update: Update, context: CallbackContext):
	if chat_id == -1001903038672:
		return 
	user = update.message.from_user
	tgUserID = user.id
	url = f"https://game.tradebotserver.xyz/bullet/api/game/pass/{tgUserID}"	
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		update.message.reply_text(result.json().get("data",{}).get("text"))
	else:
		update.message.reply_text(result.json().get("message"))


def stop(update: Update, context: CallbackContext):
	if chat_id == -1001903038672:
		return 
	user = update.message.from_user
	tgUserID = user.id
	url = f"https://game.tradebotserver.xyz/bullet/api/game/stop/{tgUserID}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		if not result.json().get("data",{}).get("isStopped", False):
			update.message.reply_text(result.json().get("data",{}).get("text"))
		else:
			link = result.json().get("data",{}).get("link")
			text = result.json().get("data",{}).get("text")
			update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Etherscan', url=link)]]), parse_mode=telegram.ParseMode.HTML)
	else:
		update.message.reply_text(result.json().get("message"))


def fix(update: Update, context: CallbackContext):
	chat_admins = update.effective_chat.get_administrators()
	if not update.effective_user in (admin.user for admin in chat_admins):
		return
	if chat_id == -1001903038672:
		return 
	url = "https://game.tradebotserver.xyz/bullet/api/admin/fix"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		link = result.json().get('data',{}).get('link', '')
		update.message.reply_text("Fix", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Fix', url=link)]]), parse_mode=telegram.ParseMode.HTML)
	else:
		update.message.reply_text(result.json().get("message"))



def leaderboard(update: Update, context):
	if chat_id == -1001903038672:
		return 
	if len(context.args)==0:
		update.message.reply_text(f"""
Usage: /leaderboard <stat>
win
loss
played
pull
pass
""")
		return
	type = context.args[0].strip()
	if type not in ["win","loss","played","pull","pass"]:
		update.message.reply_text("Invalid input")
		return 
	url = f"https://game.tradebotserver.xyz/bullet/api/leaderboard/{type}"
	result = requests.get(url)
	print(result.json())
	if result.json().get("success", False):
		tgText = result.json().get('data',{}).get('tgText', '')
		update.message.reply_text(tgText, parse_mode=telegram.ParseMode.HTML)
	else:
		update.message.reply_text(result.json().get("message"))
		

updater.dispatcher.add_handler(CommandHandler('start', start, run_async=True))
updater.dispatcher.add_handler(CommandHandler('command', start, run_async=True))
updater.dispatcher.add_handler(CommandHandler('connect', connect, run_async=True))
updater.dispatcher.add_handler(CommandHandler('flush', flush, run_async=True))
updater.dispatcher.add_handler(CommandHandler('roulette', roulette, pass_args=True, run_async=True))
updater.dispatcher.add_handler(CommandHandler('join', join, run_async=True))
updater.dispatcher.add_handler(CommandHandler('bet', bet, pass_args=True, run_async=True))
updater.dispatcher.add_handler(CommandHandler('pull', pull, run_async=True))
updater.dispatcher.add_handler(CommandHandler('pass', pass_text, run_async=True))
updater.dispatcher.add_handler(CommandHandler('stop', stop, run_async=True))
updater.dispatcher.add_handler(CommandHandler('fix', fix, run_async=True))
updater.dispatcher.add_handler(CommandHandler('leaderboard', leaderboard, run_async=True))

updater.start_polling()
