# LoliBot
# (C) Ladida

import sys, socket, string, os, atexit, random, time
import datetime, colorsys, psutil, math, requests
import subprocess, platform, multiprocessing, bs4
import xml.etree.cElementTree as ET
from colorname import colorname


class parsecommand:
	def __init__(self, arguments):
		try:
			self.args = arguments.split()
			self.command = self.args.pop(0).lower()
			self.arguments = arguments.partition(" ")[2].strip()
			self.subarguments = self.arguments.partition(" ")[2].lstrip()
		except IndexError:
			pass

	def __call__(self):
		try:
			assert (BOT.CHANNEL not in BOT.LOCKED and self.command not in self.MYCOMMANDS) or USER.OWNER()
			{**self.COMMANDS, **self.DUPLICATES, **self.MYCOMMANDS}.get(self.command, self.__INVALID)(self)
		except AttributeError:
			sendmsg("ready when you are!")
		except AssertionError:
			sendmsg("disabled")

	@staticmethod
	def __INVALID(self):
		'''command not found'''
		nobaka = "lolibot","ladida","loli","lolis","pantsu"
		baka = "make.america.great.again","ss.man"
		if USER.HOST in baka:
			sendmsg(USER.NICK+" sux")
		elif nostyle(self.command) in nobaka or nostyle(self.command)=="rate" and nostyle(self.arguments.lower()) in nobaka:
			sendmsg("kawaii!")
		else:
			sendmsg("baka!")


	def help(self):
		'''lists all user commands. use !lb help <command> for short command info'''
		if self.arguments:
			sendmsg({**self.COMMANDS,
				**self.DUPLICATES,
				**self.MYCOMMANDS}\
			.get(self.args[0].lower(), self.__INVALID).__doc__)
		else:
			sendmsg("list of commands: "+", ".join(sorted(self.COMMANDS.keys())).replace("pat","pa‍t"))

	def hi(self):
		'''says hello in japanese'''
		suffix = ("－さん","－先輩")[USER.OWNER()]
		name = "".join([chr(ord(letter)+0xFEE0) for letter in USER.NICK])
		sendmsg("お早うございます，　"+name+suffix+"！")

	def ver(self):
		'''displays bot, python, and os version'''
		sendmsg("LoliBot v0.9 / Python {} [{}] / {}".format(\
			sys.version.partition(" [")[0],
			os.environ["PROCESSOR_ARCHITECTURE"],
			platform.platform()))
		#v0.1: initial
		#v0.2: code abstraction, general format finalized
		#v0.3: commands converted from if/else (lol) to functions in dict
		#v0.4: socket fixes, buffering added
		#v0.5: misc updates; last version before loldead
		#v0.6: python 3 conversion, overall revival
		#v0.7: classes added, restartless updating implemented
		#v0.8: multiprocessing (waifu2x only) and optimized funcs/classes
		#*v0.9: more class/func optimization, list comprehensions, dict magic
		#**v1.0: ?????

	def png(self):
		'''ping'''
		sendmsg("ピング~")

	def say(self):
		'''repeats input'''
		sendmsg(self.arguments)

	def pedo(self):
		'''to be used when a pedophile is in the channel'''
		sendmsg("http://bin.smwcentral.net/u/4842/p3d0.jpg")

	def status(self):
		'''work in progress'''
		pass

	def comic(self):
		'''posts a page from one of ladida's comics'''
		comics = {"ttoa": (0,188,"comics/taleofadam/adam"),	#0-187
			"bonus": (1,5,"comics/taleofadam/BONUS_SPIEL/"),	#1-4
			"tmya": (1,29,"The%20Mario%20and%20Yoshi%20Adventure/tmya_")}	#1-28
		#try:
		#	assert self.arguments, "format: comic <type> <pg> | types: ttoa, bonus, tmya"
		#	assert self.args[0].lower() in comics.keys(), "<type> must be ttoa, bonus, or tmya"
		#	assert len(self.args)>1,
		#		"https://loli.muncher.se/"\
		#			+comics[self.args[0].lower()][2]\
		#			+str(random.randint(
		#				comics[self.args[0].lower()][0],
		#				comics[self.args[0].lower()][1]))\
		#			+".png"
		#	assert self.args[1].isdigit(), "<pg> must be a natural number"
		#	sendmsg("https://loli.muncher.se/"\
		#		+comics[self.args[0].lower()][2]\
		#		+str(int(self.args[1]))\
		#		+".png")
		#except AssertionError as comicerror:
		#	sendmsg(str(comicerror))
		try:
			sendmsg("https://loli.muncher.se/"\
				+comics[self.args[0].lower()][2]\
				+str(int(self.args[1]))\
				+".png")
		except IndexError:
			if not self.arguments:
				sendmsg("format: comic <type> <pg> | types: ttoa, bonus, tmya")
			else:
				sendmsg("https://loli.muncher.se/"\
					+comics[self.args[0].lower()][2]\
					+str(random.randint(\
						comics[self.args[0].lower()][0],
						comics[self.args[0].lower()][1]))\
					+".png")
		except KeyError:
			sendmsg("<type> must be ttoa, bonus, or tmya")
		except ValueError:
			sendmsg("<pg> must be a natural number")

	def c(self):
		'''converts between color formats. supports SNES, HEX, RGB, HSV, and color names'''
		rawcolor = self.arguments.lower()
		try:
			assert rawcolor# and "-" not in rawcolor
			if "-" in rawcolor:
				a = ""
				for water in rawcolor.lstrip("-").split():
					hexcolor = water.lstrip("#")
					if len(hexcolor) == 3:
						hexcolor = 2*hexcolor[0:1]+2*hexcolor[1:2]+2*hexcolor[2:3]
					elif len(hexcolor) < 3:
						hexcolor = hexcolor.zfill(2)*3
					else:
						hexcolor = hexcolor.zfill(6)
					hexcolor = hexcolor[len(hexcolor)-6:len(hexcolor)]
					colorR, colorG, colorB = [int(hexcolor[x*2:x*2+2], 16) for x in range(3)]
					assert colorR|colorG|colorB < 256
					snscolor = RGBtoSNS(colorR, colorG, colorB)
					a += "${},".format(snscolor)
				sendmsg(a)
				return
			colorn = False
			if rawcolor in colorname:
				rawcolor = colorname[rawcolor]
				colorn = True
			#input = SNES
			if rawcolor.startswith(("$","x","0x")) or (len(rawcolor.lstrip("$x#")) == 4 and "#" not in rawcolor):
				snscolor = rawcolor.lstrip("$x0").zfill(4)
				snscolor = snscolor[len(snscolor)-4:len(snscolor)]
				colorR, colorG, colorB = [(int(snscolor, 16)>>(x*5)&31)*8 for x in range(3)]
				assert colorR|colorG|colorB < 256
				hexcolor = RGBtoHEX(colorR, colorG, colorB)
				hue, sat, val = RGBtoHSV(colorR, colorG, colorB)
				colY, colU, colV = RGBtoYUV(colorR, colorG, colorB)
				CC,MM,YY,KK = RGBtoCMYK(colorR, colorG, colorB)
				sendmsg("{}, {}, {} | #{} | hsv {}, {}%, {}% | YUV {}, {}, {} | CMYK {}, {}, {}, {}"\
					.format(colorR,colorG,colorB,hexcolor,
						hue,sat,val,colY,colU,colV,CC,MM,YY,KK))
			#input = HEX
			elif rawcolor.startswith("#") or not set(rawcolor)&{" ",","}:
				hexcolor = rawcolor.lstrip("#")
				if len(hexcolor) == 3:
					hexcolor = 2*hexcolor[0:1]+2*hexcolor[1:2]+2*hexcolor[2:3]
				elif len(hexcolor) < 3:
					hexcolor = hexcolor.zfill(2)*3
				else:
					hexcolor = hexcolor.zfill(6)
				hexcolor = hexcolor[len(hexcolor)-6:len(hexcolor)]
				colorR, colorG, colorB = [int(hexcolor[x*2:x*2+2], 16) for x in range(3)]
				assert colorR|colorG|colorB < 256
				snscolor = RGBtoSNS(colorR, colorG, colorB)
				hue, sat, val = RGBtoHSV(colorR, colorG, colorB)
				colY, colU, colV = RGBtoYUV(colorR, colorG, colorB)
				CC,MM,YY,KK = RGBtoCMYK(colorR, colorG, colorB)
				if colorn:
					sendmsg("{}, {}, {} | {} | ${} | hsv {}, {}%, {}% | YUV {}, {}, {} | CMYK {}, {}, {}, {}"\
						.format(colorR,colorG,colorB,rawcolor.upper(),
							snscolor,hue,sat,val,colY,colU,colV,CC,MM,YY,KK))
				else:
					sendmsg("{}, {}, {} | ${} | hsv {}, {}%, {}% | YUV {}, {}, {} | CMYK {}, {}, {}, {}"\
						.format(colorR,colorG,colorB,snscolor,
							hue,sat,val,colY,colU,colV,CC,MM,YY,KK))
			#input = HSV
			elif rawcolor.startswith("hsv"):
				HSVcolor = rawcolor.replace(","," ").lstrip("hsv").split()
				valueH, valueS, valueV = [int(HSVcolor[x].rstrip(("%","")[not x]))/(100,360)[not x] for x in range(3)]
				assert max(valueH,valueS,valueV) <= 1
				colorR, colorG, colorB = [int(col*255) for col in colorsys.hsv_to_rgb(valueH, valueS, valueV)]
				hexcolor = RGBtoHEX(colorR, colorG, colorB)
				snscolor = RGBtoSNS(colorR, colorG, colorB)
				colY, colU, colV = RGBtoYUV(colorR, colorG, colorB)
				CC,MM,YY,KK = RGBtoCMYK(colorR, colorG, colorB)
				sendmsg("{}, {}, {} | #{} | ${} | YUV {}, {}, {} | CMYK {}, {}, {}, {}"\
					.format(colorR,colorG,colorB,hexcolor,
						snscolor,colY,colU,colV,CC,MM,YY,KK))
			#input = YUV
			elif rawcolor.startswith("yuv"):
				YUVcolor = rawcolor.replace(","," ").lstrip("yuv").split()
				valueY, valueU, valueV = [int(col) for col in YUVcolor][:3]
				assert valueU|valueV <= 127 and valueY <= 255
				colorR, colorG, colorB = YUVtoRGB(valueY,valueU,valueV)
				hexcolor = RGBtoHEX(colorR, colorG, colorB)
				snscolor = RGBtoSNS(colorR, colorG, colorB)
				hue, sat, val = RGBtoHSV(colorR, colorG, colorB)
				CC,MM,YY,KK = RGBtoCMYK(colorR, colorG, colorB)
				sendmsg("{}, {}, {} | #{} | ${} | hsv {}, {}%, {}% | CMYK {}, {}, {}, {}"\
					.format(colorR,colorG,colorB,hexcolor,
						snscolor,hue,sat,val,CC,MM,YY,KK))
			#input = CMYK
			elif rawcolor.startswith("cmyk"):
				CMYKcolor = rawcolor.replace(","," ").lstrip("cmyk").split()
				valueC, valueM, valueY, valueK = [float(col) for col in CMYKcolor][:4]
				assert max(valueC,valueM,valueY,valueK) <= 1
				colorR, colorG, colorB = CMYKtoRGB(valueC,valueM,valueY,valueK)
				hexcolor = RGBtoHEX(colorR, colorG, colorB)
				snscolor = RGBtoSNS(colorR, colorG, colorB)
				hue, sat, val = RGBtoHSV(colorR, colorG, colorB)
				colY, colU, colV = RGBtoYUV(colorR, colorG, colorB)
				sendmsg("{}, {}, {} | #{} | ${} | hsv {}, {}%, {}% | YUV {}, {}, {}"\
					.format(colorR,colorG,colorB,hexcolor,
						snscolor,hue,sat,val,colY,colU,colV))
			#input = RGB
			else:
				RGBcolor = rawcolor.replace(","," ").split()
				colorR, colorG, colorB = [int(col) for col in RGBcolor[:3]]
				assert colorR|colorG|colorB < 256
				hexcolor = RGBtoHEX(colorR, colorG, colorB)
				snscolor = RGBtoSNS(colorR, colorG, colorB)
				hue, sat, val = RGBtoHSV(colorR, colorG, colorB)
				colY, colU, colV = RGBtoYUV(colorR, colorG, colorB)
				CC,MM,YY,KK = RGBtoCMYK(colorR, colorG, colorB)
				sendmsg("#{} | ${} | hsv {}, {}%, {}% | YUV {}, {}, {} | CMYK {}, {}, {}, {}"\
					.format(hexcolor,snscolor,hue,sat,val,
						colY,colU,colV,CC,MM,YY,KK))
		except (ValueError, AssertionError):
			sendmsg("invalid color: R, G, B or #HEX or $SNES or hsv H, S, V or yuv Y, U, V or cmyk C, M, Y, K")

	def rei(self):
		'''iterates through a buddhist/shinto chant. works across channels'''
		sendmsg("\x02\x03"+REI.chant[REI.count])
		REI.count += (-8,1)[REI.count < len(REI.chant)-1]

	def cop(self):
		'''used to report someone to the police'''
		sendmsg("おまわりさん!! この 人 です！！\x07")

	def nyaa(self):
		'''grabs first result from nyaa or sukebei.nyaa, given a search term'''
		if self.args[0] == "sukebei":
			url = "https://sukebei.nyaa.se/?page=rss&term="+"+".join(self.args[1:])
		else:
			url = "https://www.nyaa.se/?page=rss&term="+"+".join(self.args)
		nyaa_index = ET.fromstring(requests.get(url).text)
		sendmsg(nyaa_index[0][4][0].text)

	def ava(self):
		'''posts one of ladida's random avatars'''
		sendmsg("https://loli.muncher.se/a/"\
			+random.choice(os.listdir("D:\\Dropbox\\Public\\a"))\
			.replace(" ","%20")\
			.replace("(","%28")\
			.replace(")","%29"))

	def quote(self):
		'''retrieves a random quote'''
		url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=text&lang=en"
		sendmsg(requests.get(url).text)

	def slap(self):
		'''slaps a user'''
		kaomoji = readfile("kaomoji.txt")
		if not self.arguments or BOT.NICK.lower() in self.arguments.lower():
			self.arguments = USER.NICK
		sendaction("slaps "+self.arguments+" "+random.choice(kaomoji))

	def asl(self):
		'''age of bot, sex of bot, and location of bot'''
		dt = datetime.datetime(2014, 4, 8, 14, 1, 40).timetuple()
		years = (time.time()-time.mktime(dt))/60/60/24/365.2425
		newyears = str(round(years, 3))
		age = "".join([(JP.NUM[int(item)] if item.isdigit() else "・") for item in newyears])
		sendmsg(age+"/♀/Gensokyo") #点

	def gold(self):
		'''caffie gold message in japanese'''
		sendmsg("\x02\x030,2 このメッセージは\x038,2金\x030,2のカッフィアカウントが必要です。 ") #

	def rand(self):
		'''random number. given arguments, the result is limited to a range'''
		try:
			randargs = self.arguments.replace(","," ")
			rands = randargs.split()
			randsubargs = list(randargs.partition(" "))[2].strip()
			lower = 0
			upper = 999999999
			if not randargs:
				pass
			elif not randsubargs:
				upper = int(rands[0])
				lower,upper = ((lower,upper),(upper,lower))[upper<0]
			else:
				lower = int(rands[0])
				upper = int(rands[1])
				lower,upper = ((lower,upper),(upper,lower))[lower>upper]
			sendmsg(str(random.randint(lower, upper)))
		except ValueError:
			sendmsg("invalid integer(s)!")

	def pat(self):
		'''triples each word in the input'''
		sendmsg(" ".join([pat*3 for pat in self.args]) if self.arguments else "パットパットパット")

	def choose(self):
		'''if you cant decide on something, let the bot do it for you!'''
		try:
			sendmsg(random.choice(self.args))
		except IndexError:
			sendmsg("give 1 or more whitespace-separated choices")

	def secret(self):
		''';)'''
		sendmsg("https://loli.muncher.se/himitsudesu.png")

	def w(self):
		'''ほにゃらら'''
		if not self.arguments or not self.arguments.isdigit() or len(self.arguments) > 2:
			jarajara = os.urandom(20)
		else:
			jarajara = os.urandom(int(self.arguments))
		jarajara = jarajara.replace(b"\x00",b"")\
			.replace(b"\r",b"")\
			.replace(b"\n",b"")
		s.send(b"PRIVMSG "+BOT.CHANNEL.encode()+b" :\x02\x02"+jarajara+b"\r\n")

	def bored(self):
		'''if you're bored, use this command'''
		sendmsg("Time for you to "+random.choice(readfile("bored.txt"))+"!")

	def mem(self):
		'''displays memory usage of the python process'''
		process = psutil.Process()
		mem = process.memory_full_info().uss//(2**10)
		sendmsg(repr(mem)+" KB")

	def jpdate(self):
		'''current date in japanese. given a recent era, assumes era continued to present'''
		era = {"": (0, ""),
			("imperial","kouki","koki","kōki","皇紀","こうき"): (-660,"皇紀 "),
			("heisei","平成","へいせい"): (1988,"平成 "),
			("showa","shouwa","shōwa","昭和","しょうわ"): (1925,"昭和 "),
			("taisho","taishou","taishō","大正","たいしょう"): (1911,"大正 "),
			("meiji","明治","めいじ"): (1867, "明治 ")}
		try:
			period = next(v for k,v in era.items() if self.arguments.lower() in k)
			now = datetime.date.today()
			month = JP.month(now.month)
			day = JP.day(now.day)
			year = JP.year(now.year-period[0])
			sendmsg("{}{}年 {}月 {}日".format(period[1], year, month, day))
		except StopIteration:
			sendmsg("invalid era: heisei, showa, taisho, meiji. alternatively: imperial")

	def kill(self):
		'''kill someone in IRL life'''
		sendmsg("( ﾟ▽ﾟ)o︻╦╤─ (O_O )"+(""," <--"+self.arguments)[bool(self.arguments)])

	def gelbooru(self):
		'''searches gelbooru'''
		url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags="+"+".join(self.args)
		try:
			gel_index = ET.fromstring(requests.get(url).text)
			gel_image = random.choice(\
				[x for x in gel_index if (\
					"komichi_aya" not in self.args\
					or x.attrib["rating"] not in ("e","q"))\
					or USER.HOST == "azure.colored.starlight.magic"])
			gel_tags = gel_image.attrib["tags"].split()
			sendmsg("https:"+gel_image.attrib["file_url"])
		except (IndexError, KeyError):
			sendmsg("Nobody here but us chickens!")

	def trump(self):
		'''retrieves a random Donald Trump quote. given a name, provides a Trump-esque insult'''
		http_illegal = {
			"%": "%25",
			" ": "%20",
			"\"": "%60%60",
			"#": "%23",
			"&": "%26",
			"\'": "%60",
			"+": "%2B",
			";": "%3C",
			"?": "%3F",
			"â": ","}
		for i, j in http_illegal.items():
			self.arguments = self.arguments.replace(i,j)
		modify = "personalized?q="+self.arguments if self.arguments else "random"
		url = "https://api.whatdoestrumpthink.com/api/v1/quotes/"+modify
		sendmsg(requests.get(url).text.split("\"")[3].replace("\\\\", "\\").replace("â","\'"))

	def yuri(self):
		'''WARNING: DO NOT USE. HIGHLY GRAPHIC.'''
		send("PRIVMSG "+BOT.CHANNEL+" :kouhii, hug me")

	def waifu2x(self):
		'''upscales/denoises an image using the waifu2x api. bot still usable during request'''
		method = ("-1","0","1","2","3"),("-1","1","2"),("art","photo")
		errs = ("1st argument must be -1, 0, 1, 2, or 3 (no noise -> highest noise)",
			"2nd argument must be -1, 1, or 2 (no scale, 1.6x scale, 2x scale)",
			"3rd argument must be art or photo")
		if os.path.isfile("WAIFU2X"):
			sendmsg("Please wait!")
			return
		if not self.arguments:
			sendmsg("format: waifu2x url [noise] [scale] [style]")
			return
		combined = [0,2,"art"]
		for indx in range(3):
			try:
				assert self.args[indx+1] in method[indx], errs[indx]
				combined[indx] = self.args[indx+1]
			except IndexError:
				break
			except AssertionError as invalid:
				sendmsg(str(invalid))
				return
		url = "http://waifu2x.udp.jp/api"
		body = {
			"style": combined[2].lower(),	#art, photo
			"noise": int(combined[0]),	#-1 0 1 2 3 OR none low medium high highest
			"scale": int(combined[1]),	#-1 1 2 OR none large double
			"url": self.args[0]}
		sendmsg("[waifu2x] Processing...")
		multiprocessing.Process(\
			target=waifu2x_helper,
			name="Waifu2x",
			args=(s, BOT.CHANNEL, url, BOT.HEADER, body,))\
		.start()

	def idol(self):
		'''simpler, limited version of the same kouhii command'''
		url = "https://idol.sankakucomplex.com/?tags=order:random+"+"+".join(self.args[:3])
		try:
			soup = bs4.BeautifulSoup(requests.get(url, headers=BOT.HEADER).text, "html.parser")
			assert not soup.find(string="No matching posts")
			post = random.choice(soup.find("div",attrs={"next-page-url":True}).contents[3::2])
			sendmsg(post.img["src"].replace("//i","https://is").replace("/preview",""))
		except AssertionError:
			sendmsg("No matching posts")

	def frdate(self):
		'''current date converted to french republican calendar'''
		def roman(nom):
			roman = ("","I","II","III","IV","V","VI","VII","VIII","IX")
			romanlow = roman[nom%10]
			romanhigh = roman[nom//10%10].replace("X","C").replace("V","L").replace("I","X")
			romanlong = roman[nom//100%10].replace("X","M").replace("V","D").replace("I","C")
			return romanlong+romanhigh+romanlow
		months = ("Vendémiaire","Brumaire","Frimaire",
			"Nivôse","Pluviôse","Ventôse",
			"Germinal","Floréal","Prairial",
			"Messidor","Thermidor","Fructidor","Sans-culottides")
		now = datetime.date.today().timetuple()
		year = now.tm_year-1791
		yday = now.tm_yday-(266,265)[bool(now.tm_year%4 and (not now.tm_year%100 or now.tm_year%400))]
		if yday <= 0:
			year -= 1
			yday += (366,365)[bool(now.tm_year%4 and (not now.tm_year%100 or now.tm_year%400))]
		day = yday%30
		month = months[yday//30]
		sendmsg("[WIP] {} {}, an {}".format(day, month, roman(year)))

	def archaic(self):
		'''converts kana to manyogana, and kanji to archaic forms'''
		manyo = {"":""}
		for i, j in manyo.items():
			self.arguments = self.arguments.replace(i,j)

############################################################################

	def msg(self):
		'''sends a message to a channel'''
		sendmsg(self.subarguments, self.args[0])

	def action(self):
		'''sends an action to a/the channel'''
		if self.args[0].startswith("#"):
			sendaction(self.subarguments, self.args[0])
		else:
			sendaction(self.arguments)

	def join(self):
		'''joins a channel'''
		joinchan(("#"+self.arguments,self.arguments)[self.arguments.startswith("#")])

	def part(self):
		'''leaves a/the channel'''
		if not self.arguments:
			partchan(BOT.CHANNEL, "")
		elif not self.args[0].startswith("#"):
			partchan(BOT.CHANNEL, self.arguments)
		else:
			partchan(self.args[0], self.subarguments)

	def quit(self):
		'''quits IRC and program'''
		reason = (self.arguments,"Shutting down...")[not self.arguments]
		quitIRC(0, reason)

	def restart(self):
		'''quits IRC, and restarts program'''
		reason = (self.arguments,"Restarting...")[not self.arguments]
		quitIRC(1, reason)

	def kick(self):
		'''kicks a user'''
		send("KICK ",BOT.CHANNEL," ",self.args[0]," :",self.subarguments)
		BOT.PREVCHANNEL = BOT.CHANNEL

	def nick(self):
		'''changes nickname'''
		changenick(self.args[0])

	def raw(self):
		'''sends a raw message'''
		send(self.arguments)
		BOT.PREVCHANNEL = BOT.CHANNEL

	def lock(self):
		'''prevents bot commands from being used in a channel'''
		if BOT.CHANNEL in BOT.LOCKED:
			BOT.LOCKED.remove(BOT.CHANNEL)
			sendmsg("enabled のヮの")
		else:
			BOT.LOCKED.append(BOT.CHANNEL)
			sendmsg("disabled ;_;")

	def userlock(self):
		'''prevents bot from being used by another user'''
		nhost = USER.SUX(self.args[0])
		if nhost not in BOT.SUXUSERS:
			BOT.SUXUSERS = writefile(BOT.SUXUSERS, nhost, "b_users.txt")
			sendmsg("*user locked out*", BOT.CHANNEL)
		else:
			BOT.SUXUSERS = overwritefile(BOT.SUXUSERS, nhost, "b_users.txt")
			sendmsg("*user unlocked*", BOT.CHANNEL)

	def chanban(self):
		'''bans bot from a channel'''
		try:
			if not self.arguments:
				if BOT.CHANNEL in BOT.BANNED:
					BOT.BANNED = overwritefile(BOT.BANNED, BOT.CHANNEL, "b_chans.txt")
					sendmsg("*channel unbanned*")
				else:
					BOT.BANNED = writefile(BOT.BANNED, BOT.CHANNEL, "b_chans.txt")
					sendmsg("*channel banned*")
					partchan(BOT.CHANNEL, "")
			else:
				for channel in self.args:
					channel = "#"+channel.lstrip("#")
					if channel in BOT.BANNED:
						BOT.BANNED = overwritefile(BOT.BANNED, channel, "b_chans.txt")
						sendmsg("*"+channel+" unbanned*")
					else:
						BOT.BANNED = writefile(BOT.BANNED, channel, "b_chans.txt")
						sendmsg("*"+channel+" banned*")
						partchan(channel, "")
		except ValueError:
			sendmsg("cannot locate channel in banlist!")

	def notice(self):
		'''sends a notice'''
		sendnotice(self.subarguments, self.args[0])

	def ctcp(self):
		'''sends CTCP'''
		sendctcp(self.subarguments, self.args[0])

	def update(self):
		'''restarts program without quitting IRC'''
		sendmsg("Updating...")
		liveupdate(repr(time.time()))

	def paste(self):
		'''not implemented'''
		return
		#with open("lolibot.py", encoding="ascii", errors="backslashreplace") as source:
		#	data = source.read()
		#sendmsg(uploadfile(data, BOT.HEADER))

	COMMANDS = {
		"help": help,
		"hi": hi,
		"ver": ver,
		"png": png,
		"say": say,
		"pedo": pedo,
		"status": status,
		"comic": comic,
		"c": c,
		"cop": cop,
		"rei": rei,
		"nyaa": nyaa,
		"ava": ava,
		"quote": quote,
		"slap": slap,
		"asl": asl,
		"gold": gold,
		"rand": rand,
		"pat": pat,
		"choose": choose,
		"secret": secret,
		"w": w,
		"bored": bored,
		"mem": mem,
		"jpdate": jpdate,
		"kill": kill,
		"gelbooru": gelbooru,
		"trump": trump,
		"yuri": yuri,
		"waifu2x": waifu2x,
		"idol": idol,
		"frdate": frdate
	}
	DUPLICATES = {
		"-h": help,
		"hello": hi,
		"bonjour": hi,
		"konnichiwa": hi,
		"-v": ver,
		"version": ver,
		"ping": png,
		"echo": say,
		"repeat": say,
		"p3d0": pedo,
		"col": c,
		"color": c,
		"colour": c,
		"torrent": nyaa,
		"avatar": ava,
		"random": rand,
		"randint": rand,
		"pick": choose,
		"himitsu": secret,
		"brk": w,
		"todo": bored,
		"math": w,
		"calc": w,
		"jdate": jpdate,
		"date": jpdate,
		"memory": mem,
		"post": gelbooru,
		"gel": gelbooru,
		"booru": gelbooru,
		"kouhii": yuri,
		"upscale": waifu2x,
		"waifu": waifu2x,
		"3dpd": idol,
		"3d": idol
	}
	MYCOMMANDS = {
		"msg": msg,
		"message": msg,
		"privmsg": msg,
		"action": action,
		"me": action,
		"join": join,
		"part": part,
		"leave": part,
		"quit": quit,
		"exit": quit,
		"restart": restart,
		"update": update,
		"reset": restart,
		"refresh": update,
		"reload": update,
		"kick": kick,
		"nick": nick,
		"raw": raw,
		"lock": lock,
		"chanban": chanban,
		"userlock": userlock,
		"notice": notice,
		"ctcp": ctcp,
		"paste": paste
	}

############################################################################
############################################################################

def send(*input):
	s.send(b"".join([x.encode() for x in input])+b"\r\n")

def parsemsg(rawmsg):
	splitmsg = rawmsg.lstrip(":").partition(" :")
	return splitmsg[0].split(), splitmsg[2]

def checkchan(chan):
	return USER.NICK if BOT.NICK.lower() == chan.lower() else chan

def sendmsg(*msg): #send msgs to channels/users (usually channels)
	send("PRIVMSG ",msg[1] if len(msg)>1 else BOT.CHANNEL," :\x02\x02",msg[0])

def sendaction(*msg): #send action to channels
	send("PRIVMSG ",msg[1] if len(msg)>1 else BOT.CHANNEL," :\x01ACTION \x02\x02",msg[0],"\x01")

def sendnotice(*msg): #send notice to channels/users (users highly preferred)
	send("NOTICE ",msg[1] if len(msg)>1 else BOT.CHANNEL," :\x02\x02",msg[0])

def sendctcp(*msg): #send CTCP to user or server???
	send("PRIVMSG ",msg[1] if len(msg)>1 else BOT.CHANNEL," :\x01",msg[0],"\x01")

def joinchan(chan): #join channels
	chan = chan.partition(" ")
	send("JOIN ",chan[0]," :",chan[2])

def partchan(chan, reason): #leave channels
	send("PART ",chan," :",reason)

def changenick(newnick): #change nick
	BOT.NICK = newnick
	send("NICK ",newnick)

def quitIRC(flag, reason):
	atexit.register(restartIRC, flag)
	send("QUIT :",reason)
	s.close()
	exit()

def liveupdate(inittime):
	with open("socket", "wb") as thing1:
		thing1.write(s.share(subprocess.Popen(["lolibot.bat", BOT.CHANNEL, inittime]).pid))
	s.close()
	exit()

def restartIRC(flag):
	if flag:
		time.sleep(2)
		os.startfile("lolibot.bat")
	os._exit(0)

def RGBtoHEX(r, g, b):
	return "".join([hex(x).lstrip("0x").zfill(2).upper() for x in (r,g,b)])

def RGBtoSNS(r, g, b):
	snsR, snsG, snsB = [y//8<<(x*5) for x,y in enumerate((r,g,b))]
	return hex(snsR|snsG|snsB).lstrip("0x").zfill(4).upper()

def RGBtoHSV(r, g, b):
	valH, valS, valV = colorsys.rgb_to_hsv(r/255, g/255, b/255)
	return int(valH*360), int(valS*100), int(valV*100)

def RGBtoYUV(r, g, b):
	YUV = (0.299,0.587,0.114),(-0.14713,-0.28886,0.436),(0.615, -0.51499,-0.10001)
	valY, valU, valV = [sum([y[x]*[c/255 for c in (r,g,b)][x] for x in range(3)]) for y in YUV]
	return int(valY*255), int(((valU+0.436)*255)/(0.436*2)), int(((valV+0.615)*255)/(0.615*2))

def YUVtoRGB(y, u, v):
	YUV = [y/255,(u*0.436*2)/255-0.436,(v*0.615*2)/255-0.615]
	RGB = (1,0,1.13983),(1,-0.39465,-0.5806),(1,2.03211,0)
	r,g,b = [sum([y[x]*YUV[x] for x in range(3)]) for y in RGB]
	return [int(c*255) for c in (r,g,b)]

def RGBtoCMYK(r, g, b):
	r,g,b = r/255,g/255,b/255
	K = 1-max(r,g,b)
	C = (1-r-K)/(1-K)
	M = (1-g-K)/(1-K)
	Y = (1-b-K)/(1-K)
	return [round(x,3) for x in (C,M,Y,K)]

def CMYKtoRGB(C, M, Y, K):
	r = 255*(1-C)*(1-K)
	g = 255*(1-M)*(1-K)
	b = 255*(1-Y)*(1-K)
	return [int(x) for x in (r,g,b)]

def readfile(filename):
	with open(filename) as infile:
		outfile = infile.read().split("\n")
	return outfile

def writefile(wlist, appender, filename):
	wlist.append(appender)
	with open(filename, "w") as infile:
		f = infile.write("\n".join(wlist))
	return wlist

def overwritefile(wlist, appender, filename):
	wlist.remove(appender)
	with open(filename, "w") as infile:
		f = infile.write("\n".join(wlist))
	return wlist

def uploadfile(file, header):
	upload = requests.post("http://0x0.st", headers=header, files={"file": file})
	return upload.text.rstrip("\n")

class parsename:
	def __init__(self, raw):
		try:
			self.NICK, self.NHOST = raw.split("!",1)
			self.NAME, self.HOST = self.NHOST.split("@",1)
			self.FULL = raw
		except ValueError:
			self.NICK,self.NHOST,self.NAME,self.HOST,self.FULL = (raw,)*5

	def OWNER(self):
		send("WHOIS :"+self.NICK)
		while 1:
			header, message = BOT.LOOP(False)
			if header[1] == "330":
				return (False,True)[header[4] == BOT.OWNER]
			elif "End of /WHOIS list." in message:
				return False

	@staticmethod
	def SUX(suxuser):
		send("WHOIS :"+suxuser)
		while 1:
			header, message = BOT.LOOP(False)
			if header[1] == "311":
				return header[4]+"@"+header[5]
			elif "End of /WHOIS list." in message:
				return False

def poll_output():
	infile = open("output.txt", "r+")
	output = infile.read()
	if output:
		send(output)
		infile.truncate(0)
	infile.close()

def waifu2x_helper(*inp):
	open("WAIFU2X", "w+").close()
	try:
		waifu = requests.post(inp[2], headers=inp[3], data=inp[4])
		assert waifu.status_code == requests.codes.ok
		inp[0].send(b"PRIVMSG "\
			+inp[1].encode()\
			+b" :\x02\x02[waifu2x] Done! "\
			+uploadfile(waifu.content, inp[3]).encode()\
			+b"\r\n")
	except AssertionError:
		inp[0].send(b"PRIVMSG "+inp[1].encode()+b" :\x02\x02[waifu2x] Couldn't convert url!\r\n")
	finally:
		os.remove("WAIFU2X")

def nostyle(input):
	altdic = {
		"\x02":"",
		"\x1F":"",
		"\x03":"",
		"\x0F":"",
		u"\u200E":"",
		u"\u200F":"",
		u"\u202A":"",
		u"\u202B":"",
		u"\u202D":"",
		u"\u202E":"",
		u"\u202C":"",
		u"\u200B":"",
		u"\u200D":"",
		u"\u200C":"",
		u"\u0391":"A",
		u"\u0392":"B",
		u"\u0395":"E",
		u"\u0396":"Z",
		u"\u0397":"H",
		u"\u0399":"I",
		u"\u039A":"K",
		u"\u039C":"M",
		u"\u039D":"N",
		u"\u039F":"O",
		u"\u03A1":"P",
		u"\u03A4":"T",
		u"\u03A5":"Y",
		u"\u03A7":"X",
		u"\u03BD":"v",
		u"\u03BF":"o",
		u"\u0405":"S",
		u"\u0406":"I",
		u"\u0408":"J",
		u"\u0410":"A",
		u"\u0412":"B",
		u"\u0415":"E",
		u"\u041C":"M",
		u"\u041D":"H",
		u"\u041E":"O",
		u"\u0420":"P",
		u"\u0421":"C",
		u"\u0422":"T",
		u"\u0425":"X",
		u"\u0430":"a",
		u"\u0435":"e",
		u"\u043E":"o",
		u"\u0440":"p",
		u"\u0441":"c",
		u"\u0443":"y",
		u"\u0445":"x",
		u"\u0455":"s",
		u"\u0456":"i",
		u"\u0457":"j",
		u"\u04AE":"Y"
	}
	for i, j in altdic.items():
		input = input.replace(i, j)
	return input.lower()

############################################################################
############################################################################
############################################################################

if __name__ == '__main__':
	class BOT:
		HOST = "irc.caffie.net"
		PORT = 6660 #8067
		BUFFER = b""
		NICK = "LoliBot"
		ALTNICK = "Mitsumi"
		IDENT = "yaya_nono_"
		REALNAME = "YoRHa No.2 Type B"
		OWNER = "Ladida"
		#OWNERHOST = "God.exists.her.name.is.Haruhi"
		LOCKED = [] #channels where bot is disabled. auto-handled
		BANNED = readfile("b_chans.txt") #channels where bot is banned
		SUXUSERS = readfile("b_users.txt") #users who are banned from bot
		HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'}

		@classmethod
		def LOOP(cls, verbose=True):
			while b"\r\n" not in cls.BUFFER:
				cls.BUFFER += s.recv(8)
			m, cls.BUFFER = cls.BUFFER.split(b"\r\n",1)
			print(m.decode(encoding="latin1", errors="replace")) if (m.startswith(b":") and verbose) else None
			return parsemsg(m.decode(encoding="utf-8", errors="backslashreplace"))

		@staticmethod
		def SEND(*data):
			return b"".join([x.encode() for x in data])+b"\r\n"


	class REI:
		count = 0
		chant = "4臨","7兵","8闘","9者","3皆","11陣","2列","6在","13前"

	class JP:
		NUM = '〇','一','二','三','四','五','六','七','八','九','十','十一','十二' #零
		LOW = '','一','二','三','四','五','六','七','八','九','十'
		HIGH = '','十','二十','三十','四十','五十','六十','七十','八十','九十'
		HYAKU = '','百','二百','三百','四百','五百','六百','七百','八百','九百'
		SEN = '','千','二千','三千','四千','五千','六千','七千','八千','九千'

		@classmethod
		def year(cls, input):
			yearbank = cls.SEN[input//1000]
			yearlong = cls.HYAKU[input//100%10]
			yearhigh = cls.HIGH[input//10%10]
			yearlow = cls.LOW[input%10]
			return yearbank+yearlong+yearhigh+yearlow

		@classmethod
		def month(cls, input):
			return cls.NUM[input]

		@classmethod
		def day(cls, input):
			dayhigh = cls.HIGH[input//10]
			daylow = cls.LOW[input%10]
			return dayhigh+daylow

############################################################################
############################################################################

	init = True
	ghost = False
	for retry in range(100):
		try:
			if len(sys.argv)>1:
				while not os.path.isfile("socket"):
					pass
				with open("socket", "rb") as thing2:
					s = socket.fromshare(thing2.read())
				os.remove("socket")
				init = False
				BOT.CHANNEL = sys.argv[1]
				sendmsg("Done! "+repr(time.time()-float(sys.argv[2]))[:4]+" seconds")
			else:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((BOT.HOST, BOT.PORT))
				send("NICK "+BOT.NICK)
				send("USER "+BOT.IDENT+" "+BOT.HOST+" CaffieNET :"+BOT.REALNAME)
		except (socket.error, socket.gaierror):
			time.sleep(5)
			print(retry)
			if not retry:
				atexit.register(restartIRC, 0)
				exit()
		else:
			break

############################################################################

	while 1:
		try:
			header, message = BOT.LOOP()
			send("PONG :",message) if header[0] == "PING" else None
			if init:
				if "Nickname is already in use." in message:
					send("NICK ",BOT.ALTNICK)
					ghost = True
				elif "End of /MOTD command." in message:
					if ghost:
						send("NICKSERV ghost ",BOT.NICK," ",readfile("pw.txt")[0])
						time.sleep(2)
						send("NICK ",BOT.NICK)
						ghost = False
					send("NICKSERV identify ",readfile("pw.txt")[0])
					send("MODE ",BOT.NICK," +B")
					time.sleep(2)
					[joinchan(initchan) for initchan in readfile("i_chans.txt") if not initchan.startswith(";")]
					init = False

	############################################################################

			#elif len(header) == 1:
			#elif len(header) == 2:
			elif len(header) == 3:
				if header[1] != "MODE":
					USER = parsename(header[0])
				if header[1] == "INVITE":
					BOT.CHANNEL = message
					if BOT.CHANNEL not in BOT.BANNED and USER.NHOST not in BOT.SUXUSERS:
						joinchan(BOT.CHANNEL)
						sendmsg("invited by "+USER.NICK)
				elif header[1] in ("PRIVMSG","NOTICE"):
					BOT.CHANNEL = checkchan(header[2]) #channel = current chan or nick
					try:
						splitmsg = list(message.partition(" "))
						if splitmsg[0].lower() in ("!lb",".lb") and (USER.NHOST not in BOT.SUXUSERS or USER.OWNER()):
							parsecommand(splitmsg[2].strip())()
						elif splitmsg[0].lower() == "!ping" and not splitmsg[2]:
							sendmsg("nopan!")
					except IndexError:
						sendmsg("invalid arguments")
			elif len(header) == 4:
				if message == "You're not channel operator":
					sendmsg("gimme more power!", BOT.PREVCHANNEL)
				elif message == "No such nick/channel":
					sendmsg("invalid user!", BOT.PREVCHANNEL)
			#elif len(header) == 5:
			#elif len(header) == 6:
			#elif len(header) == 7:
		except (socket.error, socket.gaierror):
			print("socket error")
			atexit.register(restartIRC, 1)
			exit()