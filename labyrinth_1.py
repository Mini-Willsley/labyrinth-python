import random, pygame, time, sys

###     CLASS DEFINITIONS     ###

class Board():
    def __init__(self):
        self.grid = []
        for i in range(7):
            minigrid = []
            for j in range(7):
                minigrid.append("")
            self.grid.append(minigrid)

        self.sprite = pygame.Surface((lengths["boardwidthheight"], lengths["boardwidthheight"]))

    def generate(self, pfixed, pmoveable):
        for i in range(0, 7, 2):
            for j in range(0, 7, 2):
                self.grid[i][j] = pfixed[0]
                pfixed = pfixed[1:]
            for j in range(1, 6, 2):
                self.grid[i][j] = pmoveable[0]
                pmoveable = pmoveable[1:]
        for i in range(1, 6, 2):
            for j in range(7):
                self.grid[i][j] = pmoveable[0]
                pmoveable = pmoveable[1:]

        self.update()
        
        return pmoveable[0]

    def move(self, pcoords, ptile, ppieces):
        if pcoords[0] == 1: # top
            temptile = self.grid[pcoords[1] * 2 + 1][-1]
            for i in range(6, 0, -1):
                self.grid[pcoords[1] * 2 + 1][i] = self.grid[pcoords[1] * 2 + 1][i - 1]
            self.grid[pcoords[1] * 2 + 1][0] = ptile
            for i in range(len(ppieces)):
                if self.gridnormalise(ppieces[i][0]) == pcoords[1]:
                    ppieces[i] = (ppieces[i][0], (ppieces[i][1] + 1) % 7)
            
        elif pcoords[0] == 2: # right
            temptile = self.grid[0][pcoords[1] * 2 + 1]
            for i in range(6):
                self.grid[i][pcoords[1] * 2 + 1] = self.grid[i + 1][pcoords[1] * 2 + 1]
            self.grid[-1][pcoords[1] * 2 + 1] = ptile
            for i in range(len(ppieces)):
                if self.gridnormalise(ppieces[i][1]) == pcoords[1]:
                    ppieces[i] = ((ppieces[i][0] - 1) % 7, ppieces[i][1])
            
        elif pcoords[0] == 3: # bot
            temptile = self.grid[pcoords[1] * 2 + 1][0]
            for i in range(6):
                self.grid[pcoords[1] * 2 + 1][i] = self.grid[pcoords[1] * 2 + 1][i + 1]
            self.grid[pcoords[1] * 2 + 1][-1] = ptile
            for i in range(len(ppieces)):
                if self.gridnormalise(ppieces[i][0]) == pcoords[1]:
                    ppieces[i] = (ppieces[i][0], (ppieces[i][1] - 1) % 7)
            
        elif pcoords[0] == 0: # left
            temptile = self.grid[-1][pcoords[1] * 2 + 1]
            for i in range(6, 0, -1):
                self.grid[i][pcoords[1] * 2 + 1] = self.grid[i - 1][pcoords[1] * 2 + 1]
            self.grid[0][pcoords[1] * 2 + 1] = ptile
            for i in range(len(ppieces)):
                if self.gridnormalise(ppieces[i][1]) == pcoords[1]:
                    ppieces[i] = ((ppieces[i][0] + 1) % 7, ppieces[i][1])
            
        self.update()
        return (temptile, ppieces)

    def update(self):
        self.sprite.fill(colours["navy"])
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.sprite.blit(self.grid[i][j].sprite, coords["tiles"][i][j])
        screen.blit(board.sprite, coords["boardtopleft"])
        arrow = pygame.Surface((lengths["individualtilewidthheight"],
                              (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 2))
        arrow.set_colorkey(colours["transparent"])
        arrow.fill(colours["transparent"])
        pygame.draw.polygon(arrow, colours["gold"], ((lengths["tilesegmentwidthheight"], (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 2),
                                                    (lengths["tilesegmentwidthheight"] * 2, (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 2),
                                                    (lengths["individualtilewidthheight"] // 2, 0)))
        for i in range(len(coords["arrows"])):
            arrow = pygame.transform.rotate(arrow, -90)
            for j in range(len(coords["arrows"][i])):
                screen.blit(arrow, coords["arrows"][i][j])

    def traverse(self, ppos, pexclude, pvalid):
        pos = ppos
        current = self.grid[ppos[0]][ppos[1]]
        if not current.shape[0] and pos[0] != 0 and pexclude != "left":
            if not self.grid[pos[0] - 1][pos[1]].shape[2] and (pos[0] - 1, pos[1]) not in pvalid:
                pvalid += self.traverse((pos[0] - 1, pos[1]), "right", pvalid + [(pos[0] - 1, pos[1])])
        if not current.shape[1] and pos[1] != 0 and pexclude != "top":
            if not self.grid[pos[0]][pos[1] - 1].shape[3] and (pos[0], pos[1] - 1) not in pvalid:
                pvalid += self.traverse((pos[0], pos[1] - 1), "bottom", pvalid + [(pos[0], pos[1] - 1)])
        if not current.shape[2] and pos[0] != 6 and pexclude != "right":
            if not self.grid[pos[0] + 1][pos[1]].shape[0] and (pos[0] + 1, pos[1]) not in pvalid:
                pvalid += self.traverse((pos[0] + 1, pos[1]), "left", pvalid + [(pos[0] + 1, pos[1])])
        if not current.shape[3] and pos[1] != 6 and pexclude != "bottom":
            if not self.grid[pos[0]][pos[1] + 1].shape[1] and (pos[0], pos[1] + 1) not in pvalid:
                pvalid += self.traverse((pos[0], pos[1] + 1), "top", pvalid + [(pos[0], pos[1] + 1)])

        valid = []
        for i in range(len(pvalid)):
            if pvalid[i] not in valid:
                valid.append(pvalid[i])
        return valid

    def gridnormalise(self, value):
        return ((value // 2) * (value % 2)) + ((value % 2) - 1)
    
class Tile(): # shape [left, top, right, bottom]
    def __init__(self, pshape, pitem):
        self.shape = pshape
        self.item = pitem
        
        self.sprite = pygame.Surface((lengths["individualtilewidthheight"], lengths["individualtilewidthheight"]))
        self.sprite.fill(colours["beige"])
        section = pygame.Surface((lengths["tilesegmentwidthheight"], lengths["tilesegmentwidthheight"]))
        section.fill(colours["sand"])
        self.sprite.blit(section, (0, 0))
        self.sprite.blit(section, (0, lengths["tilesegmentwidthheight"] * 2))
        self.sprite.blit(section, (lengths["tilesegmentwidthheight"] * 2, 0))
        self.sprite.blit(section, (lengths["tilesegmentwidthheight"] * 2, lengths["tilesegmentwidthheight"] * 2))
        if self.shape[0]:
            self.sprite.blit(section, (0, lengths["tilesegmentwidthheight"]))
        if self.shape[1]:
            self.sprite.blit(section, (lengths["tilesegmentwidthheight"], 0))
        if self.shape[2]:
            self.sprite.blit(section, (lengths["tilesegmentwidthheight"] * 2, lengths["tilesegmentwidthheight"]))
        if self.shape[3]:
            self.sprite.blit(section, (lengths["tilesegmentwidthheight"] , lengths["tilesegmentwidthheight"] * 2))

        if self.item:
            self.sprite.blit(treasuresprites[self.item], (lengths["tilesegmentwidthheight"] , lengths["tilesegmentwidthheight"]))
        
    def rotate(self, pdirection):
        if pdirection == "left":
            self.shape = self.shape[1:] + [self.shape[0]]
            self.sprite = pygame.transform.rotate(self.sprite, 90)
        if pdirection == "right":
            self.shape = [self.shape[-1]] + self.shape[0:-1]
            self.sprite = pygame.transform.rotate(self.sprite, -90)
            
class Card():
    def __init__(self, pitem):
        self.item = pitem
        boardsize = lengths["screenheight"] // 8 * 7 + lengths["screenheight"] // 16
        self.sprite = pygame.Surface(((lengths["screenwidth"] - boardsize) // 3, (lengths["screenwidth"] - boardsize) // 3 // 5 * 7))
        self.sprite.set_colorkey((colours["transparent"]))
        self.sprite.fill((colours["transparent"]))
        spriterect = self.sprite.get_rect()
        pygame.draw.rect(self.sprite, colours["sand"], spriterect, 0, 10)

        if self.item:
            pygame.draw.circle(self.sprite, colours["beige"], (spriterect.center), spriterect.centerx)
            pygame.draw.circle(self.sprite, colours["navy"], (spriterect.center), spriterect.centerx, lengths["screenwidth"] // 100)

            if self.item in treasuresprites:
                treasuresprite = pygame.transform.scale2x(treasuresprites[self.item])
            else:
                treasuresprite = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 40).render(self.item, True, colours["navy"])
            self.sprite.blit(treasuresprite, ((spriterect.width - treasuresprite.get_width()) // 2,
                                                              (spriterect.height - treasuresprite.get_height()) // 2))
          
        pygame.draw.rect(self.sprite, colours["navy"], spriterect, lengths["screenwidth"] // 100, 10)
        
class Player():
    def __init__(self, pcolour, pposition, pcards):
        self.colour = pcolour
        self.position = pposition
        self.cards = pcards
        self.sprite = pygame.Surface((lengths["screenheight"] // 24, lengths["screenheight"] // 24))
        self.sprite.set_colorkey(colours["transparent"])
        self.sprite.fill(colours["transparent"])
        pygame.draw.circle(self.sprite, self.colour, (self.sprite.get_width() // 2, self.sprite.get_height() // 2), self.sprite.get_width() // 2)
        self.update()

    def move(self, pinput):
        self.position = pinput
        self.update()

    def update(self):
        screen.blit(self.sprite, (self.position[0] * lengths["individualtilewidthheight"] + coords["boardtopleft"][0] + coords["tiles"][0][0][0] + lengths["tilesegmentwidthheight"], 
                                  self.position[1] * lengths["individualtilewidthheight"] + coords["boardtopleft"][1] + coords["tiles"][0][0][1] + lengths["tilesegmentwidthheight"]))

    def treasurefound(self):
        self.cards = self.cards[1:]

class Menu():
    def __init__(self):
        self.num = 2
        self.sprite = pygame.Surface((lengths["screenwidth"], lengths["screenheight"]))
        self.sprite.set_colorkey(colours["transparent"])
        self.sprite.fill(colours["white"])

        title = pygame.Surface((lengths["menutitlewidth"], lengths["menutitleheight"]))
        title.fill(colours["navy"])

        offset = (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 4
        for i in range(4):
            pattern = [1, 1, 1, 1]
            for j in range(random.choices([2, 3], weights = [10, 9], k = 1)[0]):
                pattern[j] = 0
            random.shuffle(pattern)
            tile = Tile(pattern, None)
            title.blit(tile.sprite, (offset + lengths["individualtilewidthheight"] * i, offset))

        text = pygame.font.Font("freesansbold.ttf", lengths["screenheight"] // 10).render("Labyrinth", True, colours["navy"])
        title.blit(text, (lengths["menutitlewidth"] // 2 - text.get_width() // 2,
                          lengths["menutitleheight"] // 2 - text.get_height() // 2))

        self.sprite.blit(title, coords["menutitle"])

        playbutton = Card("Play")
        self.sprite.blit(playbutton.sprite, coords["menuplay"])

        guidebutton = Card("Guide")
        self.sprite.blit(guidebutton.sprite, coords["menuguide"])
        self.update()

    def update(self):
        numplayers = pygame.Surface((lengths["numplayers"], lengths["numplayers"]))
        numplayers.set_colorkey(colours["transparent"])
        numplayers.fill(colours["transparent"])
        numtext = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 20).render(str(self.num), True, colours["navy"])
        numtextwhite = numtext.copy()
        numtextwhite.fill(colours["white"])
        numplayers.blit(numtextwhite, (lengths["numplayers"] // 2 - numtext.get_width() // 2,
                                       lengths["numplayers"] // 3 * 2 - numtext.get_height() // 2))
        numplayers.blit(numtext, (lengths["numplayers"] // 2 - numtext.get_width() // 2,
                                  lengths["numplayers"] // 3 * 2 - numtext.get_height() // 2))
        text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 20).render("Players:", True, colours["navy"])
        numplayers.blit(text, (lengths["numplayers"] // 2 - text.get_width() // 2,
                               lengths["numplayers"] // 3 - text.get_height() // 2))
        arrow = pygame.Surface((lengths["tilesegmentwidthheight"], lengths["tilesegmentwidthheight"]))
        arrow.set_colorkey(colours["transparent"])
        arrow.fill(colours["transparent"])
        pygame.draw.polygon(arrow, colours["navy"], ((0, 0), (0, lengths["tilesegmentwidthheight"]), (lengths["tilesegmentwidthheight"], lengths["tilesegmentwidthheight"] // 2)))
        numplayers.blit(arrow, (lengths["numplayers"] // 4 * 3 - lengths["tilesegmentwidthheight"] // 2,
                                lengths["numplayers"] // 3 * 2 - lengths["tilesegmentwidthheight"] // 2))
        arrow = pygame.transform.rotate(arrow, 180)
        numplayers.blit(arrow, (lengths["numplayers"] // 4 - lengths["tilesegmentwidthheight"] // 2,
                                lengths["numplayers"] // 3 * 2 - lengths["tilesegmentwidthheight"] // 2))
        self.sprite.blit(numplayers, coords["menuplayers"])

class Winscreen():
    def __init__(self):
        self.sprite = pygame.Surface((lengths["winscreenwidth"],
                                      lengths["winscreenheight"]))
        self.sprite.fill(colours["navy"])
        miniwinscreen = pygame.Surface((lengths["cardwidth"] * 5 - lengths["cardwidth"] // 2,
                                        lengths["individualtilewidthheight"] * 3 - lengths["cardwidth"] // 2))
        miniwinscreen.fill((colours["sand"]))
        self.sprite.blit(miniwinscreen, (lengths["winscreenwidth"] // 2 - miniwinscreen.get_width() // 2,
                                       lengths["winscreenheight"] // 2 - miniwinscreen.get_height() // 2))
    def draw(self, pwinner):
        sprite = pygame.transform.scale2x(pwinner.sprite)
        text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 20).render(f"{players.index(pwinner) + 1}", True, colours["navy"])
        sprite.blit(text, ((sprite.get_width() - text.get_width()) // 2, (sprite.get_height() - text.get_height()) // 2))
        text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 20).render("Player ", True, colours["navy"])
        textagain = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 20).render(" Wins", True, colours["navy"])
        bigtext = pygame.Surface((text.get_width() + textagain.get_width() + sprite.get_width(), sprite.get_height()))
        bigtext.set_colorkey(colours["transparent"])
        bigtext.fill(colours["transparent"])
        bigtext.blit(text, (0, (bigtext.get_height() - text.get_height()) // 2))
        bigtext.blit(textagain, (text.get_width() + sprite.get_width(), (bigtext.get_height() - textagain.get_height()) // 2))
        bigtext.blit(sprite, (text.get_width(), 0))
        self.sprite.blit(bigtext, (lengths["winscreenwidth"] // 2 - bigtext.get_width() // 2,
                              lengths["winscreenheight"] // 3 - bigtext.get_height() // 2))

        text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 40).render("Click To Continue", True, colours["navy"])
        self.sprite.blit(text, (lengths["winscreenwidth"] // 2 - text.get_width() // 2,
                              lengths["winscreenheight"] // 3 * 2 - text.get_height() // 2))
        screen.blit(self.sprite, coords["winscreen"])

class Guide():
    def __init__(self):
        self.helpinghand = pygame.Surface((lengths["cardwidth"], lengths["cardheight"]))
        self.helpinghand.set_colorkey(colours["transparent"])
        self.helpinghand.fill(colours["transparent"])
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] // 9 * 2, lengths["cardheight"] - lengths["cardheight"] // 15 * 2), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 5, lengths["cardheight"] - lengths["cardheight"] // 15 * 2), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 10, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] // 8, lengths["cardheight"] // 2 + lengths["cardheight"] // 11)))
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] // 8, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] // 6 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11),
                                                                 (lengths["cardwidth"] // 9 * 2, lengths["cardheight"] // 2 - lengths["cardheight"] // 17), 
                                                                 (lengths["cardwidth"] // 14, lengths["cardheight"] // 2 - lengths["cardheight"] // 17)))
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] // 6 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] // 8 * 4, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] // 8 * 4, lengths["cardheight"] // 12 * 2), 
                                                                 (lengths["cardwidth"] // 6 * 2, lengths["cardheight"] // 12 * 2)))
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] // 8 * 4, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 5 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 5 * 2, lengths["cardheight"] // 2 - lengths["cardheight"] // 17), 
                                                                 (lengths["cardwidth"] // 8 * 4, lengths["cardheight"] // 2 - lengths["cardheight"] // 17)))
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] - lengths["cardwidth"] // 5 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 8 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 8 * 2, lengths["cardheight"] // 2 - lengths["cardheight"] // 46), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 5 * 2, lengths["cardheight"] // 2 - lengths["cardheight"] // 46)))
        pygame.draw.polygon(self.helpinghand, colours["black"], ((lengths["cardwidth"] - lengths["cardwidth"] // 8 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 11, lengths["cardheight"] // 2 + lengths["cardheight"] // 11), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 11, lengths["cardheight"] // 2 + lengths["cardheight"] // 70), 
                                                                 (lengths["cardwidth"] - lengths["cardwidth"] // 8 * 2, lengths["cardheight"] // 2 + lengths["cardheight"] // 70)))
        pygame.draw.circle(self.helpinghand, colours["black"], (lengths["cardwidth"] // 8, lengths["cardheight"] // 16 * 8), lengths["cardheight"] // 16)
        pygame.draw.circle(self.helpinghand, colours["black"], (lengths["cardwidth"] // 12 * 5, lengths["cardheight"] // 11 * 2), lengths["cardheight"] // 16)
        pygame.draw.circle(self.helpinghand, colours["black"], (lengths["cardwidth"] // 9 * 4, lengths["cardheight"] // 16 * 8), lengths["cardheight"] // 16)
        pygame.draw.circle(self.helpinghand, colours["black"], (lengths["cardwidth"] // 10 * 6, lengths["cardheight"] // 2), lengths["cardheight"] // 16)
        pygame.draw.circle(self.helpinghand, colours["black"], (lengths["cardwidth"] // 6 * 5, lengths["cardheight"] // 2 + lengths["cardheight"] // 35), lengths["cardheight"] // 16)

        self.patch = self.helpinghand.copy()
        self.patch.fill(colours["white"])

    def drawguide(self, num, i):
        match num:
            case 0:
                screen.blit(self.helpinghand, coords["menuplayguide"])
                screen.blit(self.helpinghand, coords["menurightarrowguide"])
                screen.blit(self.helpinghand, coords["menuleftarrowguide"])
                text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 40).render("Click Play To Begin", True, colours["black"])
                screen.blit(text, ((coords["menuplay"][0] - text.get_width()) // 2, coords["menuplay"][1] + (lengths["cardheight"] - text.get_height()) // 2))
            case 1:
                screen.blit(self.helpinghand, coords["gamestartguide"])
            case 2:
                board.update()
                for i in range(len(players)):
                    players[i].update()
                screen.blit(self.helpinghand, coords["gameleftbuttonguide"])
                screen.blit(self.helpinghand, coords["gamerightbuttonguide"])
                screen.blit(self.helpinghand, coords["gametileguide"])
            case 3:
                screen.blit(self.patch, coords["gameleftbuttonguide"])
                screen.blit(self.patch, coords["gamerightbuttonguide"])
                screen.blit(self.patch, coords["gametileguide"])
                screen.blit(helpbutton.sprite, coords["helpbutton"])
                screen.blit(rightbutton, coords["leftbutton"])
                screen.blit(leftbutton, coords["rightbutton"])
            case 4:
                tempval = board.traverse(players[i].position, None, [players[i].position])
                tempval = tempval[random.randint(0, len(tempval) - 1)]
                screen.blit(self.helpinghand, (coords["tiles"][tempval[0]][tempval[1]][0] + coords["tilestopleft"][0],
                                               coords["tiles"][tempval[0]][tempval[1]][1] + coords["tilestopleft"][1]))



###     FUNCTION DEFINITIONS     ###

def updatescore(pplayer):
    scores = pygame.Surface((lengths["cardwidth"], lengths["scoresheight"]))
    scores.set_colorkey(colours["transparent"])
    scores.fill(colours["white"])
    ygap = (lengths["scoresheight"] - (len(players) * 2 * lengths["tilesegmentwidthheight"])) // (len(players) + 1)
    xgap = (lengths["cardwidth"] - (lengths["tilesegmentwidthheight"] * 2 + lengths["tilesegmentwidthheight"] // 2)) // 3
    for i in range(len(players)):
        playersprite = pygame.transform.scale2x(players[i].sprite)
        text = pygame.font.Font("freesansbold.ttf", lengths["screenwidth"] // 40).render(str(len(deck) // len(players) - len(players[i].cards)), True, colours["black"])
        playersprite.blit(text, (lengths["tilesegmentwidthheight"] - text.get_width() // 2,
                                 lengths["tilesegmentwidthheight"] - text.get_height() // 2))
        scores.blit(playersprite, (lengths["tilesegmentwidthheight"] // 2 + xgap * 2,
                                   ygap * (i + 1) + lengths["tilesegmentwidthheight"] * 2 * i))
    arrow = pygame.Surface((lengths["tilesegmentwidthheight"] // 2, lengths["tilesegmentwidthheight"]))
    arrow.set_colorkey(colours["transparent"])
    arrow.fill(colours["transparent"])
    pygame.draw.polygon(arrow, colours["navy"], ((0, 0), (0, lengths["tilesegmentwidthheight"]),
                                                 (lengths["tilesegmentwidthheight"] // 2, lengths["tilesegmentwidthheight"] // 2)))
    scores.blit(arrow, (xgap,
                        ygap * (pplayer + 1) + lengths["tilesegmentwidthheight"] * 2 * pplayer + lengths["tilesegmentwidthheight"] // 2))
    screen.blit(scores, coords["scores"])

def createplayers(deck, num):
    cards = len(deck) // num
    players = []
    if num >= 1:
        players.append(playeryellow := Player(colours["yellow"], (0, 0), deck[:cards]))
    if num >= 2:
        players.append(playerred := Player(colours["red"], (6, 0), deck[cards:cards * 2]))
    if num >= 3:
        players.append(playergreen := Player(colours["green"], (0, 6), deck[cards * 2:cards * 3]))
    if num >= 4:
        players.append(playerblue := Player(colours["blue"], (6, 6), deck[cards * 3:]))
    playerpos = []
    for i in range(len(players)):
        playerpos.append(players[i].position)
    return [players, playerpos]

def getpygameinput(pstate):
    while True:
        events = pygame.event.get()
        for i in range(len(events)):
            if events[i].type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if events[i].type == pygame.MOUSEBUTTONDOWN:
                if pstate == "game":
                    inp = translategameinput(events[i].pos)
                elif pstate == "menu":
                    inp = translatemenuinput(events[i].pos)
                if inp:
                    return inp

def translategameinput(pcoords):
    for i in range(len(coords["arrows"])):
        for j in range(len(coords["arrows"][i])):
            if i % 2 == 1:
                if pcoords[0] > coords["arrows"][i][j][0] and pcoords[0] < coords["arrows"][i][j][0] + lengths["individualtilewidthheight"]:
                    if pcoords[1] > coords["arrows"][i][j][1] and pcoords[1] < coords["arrows"][i][j][1] + lengths["screenheight"] // 32:
                        return ["tile", (i, j)]
            elif i % 2 == 0:
                if pcoords[0] > coords["arrows"][i][j][0] and pcoords[0] < coords["arrows"][i][j][0] + lengths["screenheight"] // 32:
                    if pcoords[1] > coords["arrows"][i][j][1] and pcoords[1] < coords["arrows"][i][j][1] + lengths["individualtilewidthheight"]:
                        return ["tile", (i, j)]

    if coords["leftbutton"][0] < pcoords[0] < coords["leftbutton"][0] + lengths["tilesegmentwidthheight"]:
        if coords["leftbutton"][1] < pcoords[1] < coords["leftbutton"][1] + lengths["tilesegmentwidthheight"]:
            return ["button", "left"]

    if coords["rightbutton"][0] < pcoords[0] < coords["rightbutton"][0] + lengths["tilesegmentwidthheight"]:
        if coords["rightbutton"][1] < pcoords[1] < coords["rightbutton"][1] + lengths["tilesegmentwidthheight"]:
            return ["button", "right"]

    if coords["helpbutton"][0] < pcoords[0] < coords["helpbutton"][0] + lengths["cardwidth"]:
        if coords["helpbutton"][1] < pcoords[1] < coords["helpbutton"][1] + lengths["cardheight"]:
            return ["help"]    

    pcoords = (pcoords[0] - coords["boardtopleft"][0], pcoords[1] - coords["boardtopleft"][1])
    for i in range(len(coords["tiles"])):
        for j in range(len(coords["tiles"][i])):
            if pcoords[0] > coords["tiles"][i][j][0] and pcoords[0] < coords["tiles"][i][j][0] + lengths["individualtilewidthheight"]:
                if pcoords[1] > coords["tiles"][i][j][1] and pcoords[1] < coords["tiles"][i][j][1] + lengths["individualtilewidthheight"]:
                    return ["player", (i, j)]

    return "none"

def translatemenuinput(pcoords):
    if pcoords[0] > coords["menuleftarrow"][0] and pcoords[0] < coords["menuleftarrow"][0] + lengths["tilesegmentwidthheight"] and pcoords[1] > coords["menuleftarrow"][1] and pcoords[1] < coords["menuleftarrow"][1] + lengths["tilesegmentwidthheight"]:
        return "decrease"
    elif pcoords[0] > coords["menurightarrow"][0] and pcoords[0] < coords["menurightarrow"][0] + lengths["tilesegmentwidthheight"] and pcoords[1] > coords["menurightarrow"][1] and pcoords[1] < coords["menurightarrow"][1] + lengths["tilesegmentwidthheight"]:
        return "increase"
    elif pcoords[0] > coords["menuplay"][0] and pcoords[0] < coords["menuplay"][0] + lengths["cardwidth"] and pcoords[1] > coords["menuplay"][1] and pcoords[1] < coords["menuplay"][1] + lengths["cardheight"]:
        return "play"
    elif pcoords[0] > coords["menuguide"][0] and pcoords[0] < coords["menuguide"][0] + lengths["cardwidth"] and pcoords[1] > coords["menuguide"][1] and pcoords[1] < coords["menuguide"][1] + lengths["cardheight"]:
        return "guide"

def drawmultilinetext(string, pattern, fontsize, colour):
    string = string.split(" ")
    for i in range(len(string)):
        string[i] = " " + string[i] + " "
        text = pygame.font.Font("freesansbold.ttf", fontsize).render(string[i], True, colour)
        string[i] = pygame.Surface((text.get_width(), text.get_height()))
        string[i].set_colorkey(colours["transparent"])
        string[i].fill(colours["transparent"])
        string[i].blit(text, (0, 0))
    lis = []
    height = string[0].get_height()
    for i in range(len(pattern)):
        width = 0
        for j in range(pattern[i]):
            width += string[j].get_width()
        surf = pygame.Surface((width, height))
        surf.set_colorkey(colours["transparent"])
        surf.fill(colours["transparent"])
        buffer = 0
        for j in range(pattern[i]):
            surf.blit(string[j], (buffer, 0))
            buffer += string[j].get_width()
        string = string[pattern[i]:]
        lis.append(surf)
    width = lis[0].get_width()
    for i in range(1, len(lis)):
        if lis[i].get_width() > width:
            width = lis[i].get_width()
    base = pygame.Surface((width, height * len(pattern)))
    base.set_colorkey(colours["transparent"])
    base.fill(colours["transparent"])
    for i in range(len(lis)):
        base.blit(lis[i], ((width - lis[i].get_width()) // 2, height * i))
    return base

###     ASSET SETUP     ###

pygame.init()
lengths = {"screenwidth" : 800,
           "screenheight" : 600}

lengths["boardwidthheight"] = lengths["screenheight"] // 8 * 7 + lengths["screenheight"] // 16
lengths["tileswidthheight"] = lengths["screenheight"] // 8 * 7
lengths["individualtilewidthheight"] = lengths["screenheight"] // 8
lengths["tilesegmentwidthheight"] = lengths["individualtilewidthheight"] // 3
lengths["cardwidth"] = (lengths["screenwidth"] - lengths["boardwidthheight"]) // 3
lengths["cardheight"] = (lengths["screenwidth"] - lengths["boardwidthheight"]) // 3 // 5 * 7
lengths["menutitlewidth"] = (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 2 + lengths["individualtilewidthheight"] * 4
lengths["menutitleheight"] = (lengths["boardwidthheight"] - lengths["tileswidthheight"]) // 2 + lengths["individualtilewidthheight"]
lengths["numplayers"] = lengths["individualtilewidthheight"] * 3
lengths["winscreenwidth"] = lengths["cardwidth"] * 5
lengths["winscreenheight"] = lengths["individualtilewidthheight"] * 3
lengths["treasurespritewidthheight"] = lengths["screenwidth"] // 32

coords = {"boardtopleft" : (lengths["screenwidth"] // 2 - lengths["boardwidthheight"] // 2,
                            lengths["screenheight"] // 2 - lengths["boardwidthheight"] // 2),
          "tiles" : [],
          "arrows" : []}
coords["boardtopright"] = (coords["boardtopleft"][0] + lengths["boardwidthheight"],
                           coords["boardtopleft"][1])
coords["boardbottomleft"] = (coords["boardtopleft"][0],
                             coords["boardtopleft"][1] + lengths["boardwidthheight"])
coords["boardbottomright"] = (coords["boardtopleft"][0] + lengths["boardwidthheight"],
                              coords["boardtopleft"][1] + lengths["boardwidthheight"])
coords["tilestopleft"] = (coords["boardtopleft"][0] + lengths["screenheight"] // 32,
                         coords["boardtopleft"][1] + lengths["screenheight"] // 32)
coords["tilestopright"] = (coords["tilestopleft"][0] + lengths["tileswidthheight"],
                           coords["tilestopleft"][1])
coords["tilesbottomleft"] = (coords["tilestopleft"][0],
                             coords["tilestopleft"][1] + lengths["tileswidthheight"])
coords["tilesbottomright"] = (coords["tilestopleft"][0] + lengths["tileswidthheight"],
                              coords["tilestopleft"][1] + lengths["tileswidthheight"])

coords["outtile"] = ((lengths["screenwidth"] - lengths["boardwidthheight"]) // 4 - lengths["individualtilewidthheight"] // 2,
                      coords["tilesbottomright"][1] - 5 * lengths["tilesegmentwidthheight"])

coords["leftbutton"] = ((lengths["screenwidth"] - lengths["boardwidthheight"]) // 4 - lengths["individualtilewidthheight"] // 2,
                       coords["tilesbottomright"][1] - lengths["tilesegmentwidthheight"])

coords["rightbutton"] = ((lengths["screenwidth"] - lengths["boardwidthheight"]) // 4 - lengths["individualtilewidthheight"] // 2 + 2 * lengths["tilesegmentwidthheight"],
                       coords["tilesbottomright"][1] - lengths["tilesegmentwidthheight"])

coords["card"] = ((lengths["screenwidth"] - lengths["boardwidthheight"]) // 4 - lengths["cardwidth"] // 2,
                   coords["tilestopleft"][1])

coords["scores"] = ((lengths["screenwidth"] - lengths["boardwidthheight"]) // 4 - lengths["individualtilewidthheight"] // 2,
                     coords["card"][1] + lengths["cardheight"])

coords["menutitle"] = (lengths["screenwidth"] // 2 - lengths["menutitlewidth"] // 2,
                       lengths["screenheight"] // 4 - lengths["menutitleheight"] // 2)
coords["menuplayers"] = (lengths["screenwidth"] // 2 - lengths["numplayers"] // 2,
                         lengths["screenheight"] // 2 - lengths["numplayers"] // 2)
coords["menuplay"] = (lengths["screenwidth"] // 7 * 3 - lengths["cardwidth"] // 2,
                      lengths["screenheight"] // 5 * 4 - lengths["cardheight"] // 2)
coords["menuguide"] = (lengths["screenwidth"] // 7 * 4 - lengths["cardwidth"] // 2,
                       lengths["screenheight"] // 5 * 4 - lengths["cardheight"] // 2)
coords["menurightarrow"] = (coords["menuplayers"][0] + lengths["numplayers"] // 4 * 3 - lengths["tilesegmentwidthheight"] // 2,
                            coords["menuplayers"][1] + lengths["numplayers"] // 3 * 2 - lengths["tilesegmentwidthheight"] // 2)
coords["menuleftarrow"] = (coords["menuplayers"][0] + lengths["numplayers"] // 4 - lengths["tilesegmentwidthheight"] // 2,
                           coords["menuplayers"][1] + lengths["numplayers"] // 3 * 2 - lengths["tilesegmentwidthheight"] // 2)
coords["winscreen"] = (lengths["screenwidth"] // 2 - lengths["winscreenwidth"] // 2,
                       lengths["screenheight"] // 2 - lengths["winscreenheight"] // 2)
coords["menuleftarrowguide"] = (coords["menuleftarrow"][0] - lengths["cardwidth"] // 5,
                                coords["menuleftarrow"][1])
coords["menurightarrowguide"] = (coords["menurightarrow"][0] - lengths["cardwidth"] // 5,
                                 coords["menurightarrow"][1])
coords["menuplayguide"] = (coords["menuplay"][0] + lengths["cardwidth"] // 3,
                           coords["menuplay"][1] + lengths["cardheight"] // 2)
coords["gamestartguide"] = (lengths["screenwidth"] // 2,
                            lengths["screenheight"] // 2)
coords["gameleftbuttonguide"] = (coords["leftbutton"][0] - lengths["cardwidth"] // 10,
                                 coords["leftbutton"][1])
coords["gamerightbuttonguide"] = (coords["rightbutton"][0] - lengths["cardwidth"] // 10,
                                  coords["rightbutton"][1])
coords["gametileguide"] = (coords["tilesbottomright"][0] - lengths["cardwidth"] // 5,
                           coords["tilesbottomright"][1] - lengths["cardheight"])
coords["helpbutton"] = ((lengths["screenwidth"] - (lengths["screenwidth"] - lengths["boardwidthheight"]) // 4) - lengths["cardwidth"] // 2,
                         coords["tilesbottomright"][1] - lengths["cardheight"])

lengths["scoresheight"] = coords["outtile"][1] - coords["card"][1] - lengths["cardheight"]

for i in range(7):
    minitiles = []
    for j in range(7):
        minitiles.append((i * lengths["individualtilewidthheight"] + lengths["screenheight"] // 32, j * lengths["individualtilewidthheight"] + lengths["screenheight"] // 32))
    coords["tiles"].append(minitiles)

miniarrows = []
for i in range(1, 7, 2):
    miniarrows.append((coords["boardtopleft"][0],
                             coords["tilestopleft"][1] + i * lengths["individualtilewidthheight"]))
coords["arrows"].append(miniarrows)
miniarrows = []
for i in range(1, 7, 2):
    miniarrows.append((coords["tilestopleft"][0]  + i * lengths["individualtilewidthheight"],
                             coords["boardtopleft"][1]))
coords["arrows"].append(miniarrows)
miniarrows = []
for i in range(1, 7, 2):
    miniarrows.append((coords["tilestopright"][0],
                             coords["tilestopleft"][1] + i * lengths["individualtilewidthheight"]))
coords["arrows"].append(miniarrows)
miniarrows = []
for i in range(1, 7, 2):
    miniarrows.append((coords["tilesbottomleft"][0] + i * lengths["individualtilewidthheight"],
                             coords["tilesbottomleft"][1]))
coords["arrows"].append(miniarrows)

colours = {"transparent" : (69, 69, 69),
           "black" : (10, 10, 10),
           "white" : (220, 220, 220),
           "sand" : (219,154,89),
           "beige" : (246,215,176),
           "navy" : (0, 0, 48),
           "red" : (245, 15, 23),
           "blue" : (3, 36, 247),
           "yellow" : (221, 209, 2),
           "green" : (4, 168, 74),
           "gold" : (234, 221, 21),
           "sapphire" : (22, 45, 232),
           "creme" : (247, 238, 152),
           "offwhite" : (236, 237, 224),
           "purple" : (145, 21, 231),
           "rust" : (202, 134, 16),
           "dark" : (35, 1, 3),
           "emerald" : (32, 212, 45),
           "brown" : (134, 62, 12),
           "grey" : (123, 123, 123),
           "pink" : (238, 187, 213)}

treasurecoords = {}
for i in range(32):
    treasurecoords[i] = int(i / 32 * lengths["treasurespritewidthheight"]) + bool(i)

ring = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
ring.fill(colours["transparent"])
ring.set_colorkey(colours["transparent"])
pygame.draw.circle(ring, colours["gold"], (treasurecoords[16], treasurecoords[18]), treasurecoords[12], treasurecoords[3])
pygame.draw.circle(ring, colours["sapphire"], (treasurecoords[16], treasurecoords[6]), treasurecoords[4])

genie = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
genie.fill(colours["transparent"])
genie.set_colorkey(colours["transparent"])
pygame.draw.polygon(genie, colours["gold"], ((treasurecoords[7], treasurecoords[25]), (treasurecoords[24], treasurecoords[25]), (treasurecoords[15], treasurecoords[17])))
pygame.draw.polygon(genie, colours["gold"], ((treasurecoords[4], treasurecoords[10]), (treasurecoords[15], treasurecoords[12]), (treasurecoords[15], treasurecoords[20])))
pygame.draw.circle(genie, colours["gold"], (treasurecoords[17], treasurecoords[17]), treasurecoords[6])
pygame.draw.circle(genie, colours["gold"], (treasurecoords[23], treasurecoords[15]), treasurecoords[6], treasurecoords[3])

crown = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
crown.fill(colours["transparent"])
crown.set_colorkey(colours["transparent"])
pygame.draw.polygon(crown, colours["gold"], ((treasurecoords[0], treasurecoords[24]), (treasurecoords[15], treasurecoords[24]), (treasurecoords[5], treasurecoords[7])))
pygame.draw.polygon(crown, colours["gold"], ((treasurecoords[6], treasurecoords[24]), (treasurecoords[25], treasurecoords[24]), (treasurecoords[15], treasurecoords[7])))
pygame.draw.polygon(crown, colours["gold"], ((treasurecoords[16], treasurecoords[24]), (treasurecoords[31], treasurecoords[24]), (treasurecoords[26], treasurecoords[7])))
pygame.draw.circle(crown, colours["sapphire"], (treasurecoords[16], treasurecoords[19]), treasurecoords[3])

candle = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
candle.fill(colours["transparent"])
candle.set_colorkey(colours["transparent"])
pygame.draw.polygon(candle, colours["creme"], ((treasurecoords[1], treasurecoords[18]), (treasurecoords[5], treasurecoords[18]), (treasurecoords[5], treasurecoords[0]), (treasurecoords[1], treasurecoords[0])))
pygame.draw.polygon(candle, colours["creme"], ((treasurecoords[13], treasurecoords[18]), (treasurecoords[17], treasurecoords[18]), (treasurecoords[17], treasurecoords[0]), (treasurecoords[13], treasurecoords[0])))
pygame.draw.polygon(candle, colours["creme"], ((treasurecoords[26], treasurecoords[18]), (treasurecoords[30], treasurecoords[18]), (treasurecoords[30], treasurecoords[0]), (treasurecoords[26], treasurecoords[0])))
pygame.draw.polygon(candle, colours["gold"], ((treasurecoords[0], treasurecoords[31]), (treasurecoords[31], treasurecoords[31]), (treasurecoords[15], treasurecoords[24])))
pygame.draw.polygon(candle, colours["gold"], ((treasurecoords[13], treasurecoords[31]), (treasurecoords[18], treasurecoords[31]), (treasurecoords[18], treasurecoords[18]), (treasurecoords[13], treasurecoords[18])))
pygame.draw.polygon(candle, colours["gold"], ((treasurecoords[1], treasurecoords[18]), (treasurecoords[30], treasurecoords[18]), (treasurecoords[15], treasurecoords[22])))

ghost = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
ghost.fill(colours["transparent"])
ghost.set_colorkey(colours["transparent"])
pygame.draw.circle(ghost, colours["offwhite"], (treasurecoords[16], treasurecoords[13]), treasurecoords[11])
pygame.draw.polygon(ghost, colours["offwhite"], ((treasurecoords[5], treasurecoords[13]), (treasurecoords[27], treasurecoords[13]), (treasurecoords[27], treasurecoords[28]), (treasurecoords[5], treasurecoords[28])))
for i in range(6):
    pygame.draw.circle(ghost, colours["offwhite"], (treasurecoords[6 + i * 4], treasurecoords[28]), treasurecoords[2])

keys = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
keys.fill(colours["transparent"])
keys.set_colorkey(colours["transparent"])
pygame.draw.circle(keys, colours["rust"], (treasurecoords[16], treasurecoords[8]), treasurecoords[6], treasurecoords[3])
pygame.draw.line(keys, colours["rust"], (treasurecoords[15], treasurecoords[14]), (treasurecoords[15], treasurecoords[29]), treasurecoords[2])
pygame.draw.polygon(keys, colours["rust"], ((treasurecoords[15], treasurecoords[29]), (treasurecoords[15], treasurecoords[26]), (treasurecoords[19], treasurecoords[26]), (treasurecoords[19], treasurecoords[29])))
pygame.draw.line(keys, colours["rust"], (treasurecoords[15], treasurecoords[22]), (treasurecoords[18], treasurecoords[22]), treasurecoords[2])

skull = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
skull.fill(colours["transparent"])
skull.set_colorkey(colours["transparent"])
pygame.draw.circle(skull, colours["offwhite"], (treasurecoords[15], treasurecoords[12]), treasurecoords[11])
pygame.draw.polygon(skull, colours["offwhite"], ((treasurecoords[10], treasurecoords[12]), (treasurecoords[20], treasurecoords[12]), (treasurecoords[20], treasurecoords[28]), (treasurecoords[10], treasurecoords[28])))
pygame.draw.circle(skull, colours["dark"], (treasurecoords[10], treasurecoords[12]), treasurecoords[3])
pygame.draw.circle(skull, colours["dark"], (treasurecoords[20], treasurecoords[12]), treasurecoords[3])

moth = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
moth.fill(colours["transparent"])
moth.set_colorkey(colours["transparent"])
pygame.draw.circle(moth, colours["dark"], (treasurecoords[16], treasurecoords[19]), treasurecoords[5])
pygame.draw.circle(moth, colours["rust"], (treasurecoords[16], treasurecoords[12]), treasurecoords[5])
pygame.draw.line(moth, colours["rust"], (treasurecoords[15], treasurecoords[12]), (treasurecoords[20], treasurecoords[4]), treasurecoords[2])
pygame.draw.line(moth, colours["rust"], (treasurecoords[15], treasurecoords[12]), (treasurecoords[10], treasurecoords[4]), treasurecoords[2])
pygame.draw.polygon(moth, colours["rust"], ((treasurecoords[16], treasurecoords[12]), (treasurecoords[12], treasurecoords[12]), (treasurecoords[4], treasurecoords[27]), (treasurecoords[10], treasurecoords[25])))
pygame.draw.polygon(moth, colours["rust"], ((treasurecoords[20], treasurecoords[12]), (treasurecoords[16], treasurecoords[12]), (treasurecoords[20], treasurecoords[25]), (treasurecoords[26], treasurecoords[27])))

gem = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
gem.fill(colours["transparent"])
gem.set_colorkey(colours["transparent"])
pygame.draw.polygon(gem, colours["emerald"], ((treasurecoords[4], treasurecoords[13]), (treasurecoords[26], treasurecoords[13]), (treasurecoords[15], treasurecoords[24])))
pygame.draw.polygon(gem, colours["emerald"], ((treasurecoords[4], treasurecoords[13]), (treasurecoords[10], treasurecoords[13]), (treasurecoords[10], treasurecoords[7])))
pygame.draw.polygon(gem, colours["emerald"], ((treasurecoords[20], treasurecoords[13]), (treasurecoords[26], treasurecoords[13]), (treasurecoords[20], treasurecoords[7])))
pygame.draw.polygon(gem, colours["emerald"], ((treasurecoords[10], treasurecoords[7]), (treasurecoords[20], treasurecoords[7]), (treasurecoords[20], treasurecoords[13]), (treasurecoords[10], treasurecoords[13])))

sword = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
sword.fill(colours["transparent"])
sword.set_colorkey(colours["transparent"])
pygame.draw.line(sword, colours["brown"], (treasurecoords[15], treasurecoords[3]), (treasurecoords[15], treasurecoords[7]), treasurecoords[2])
pygame.draw.line(sword, colours["offwhite"], (treasurecoords[15], treasurecoords[7]), (treasurecoords[15], treasurecoords[24]), treasurecoords[5])
pygame.draw.polygon(sword, colours["offwhite"], ((treasurecoords[15], treasurecoords[30]), (treasurecoords[13], treasurecoords[24]) ,(treasurecoords[17], treasurecoords[24])))
pygame.draw.line(sword, colours["gold"], (treasurecoords[11], treasurecoords[7]), (treasurecoords[19], treasurecoords[7]), treasurecoords[2])
pygame.draw.circle(sword, colours["gold"], (treasurecoords[16], treasurecoords[3]), treasurecoords[2])

lizard = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
lizard.fill(colours["transparent"])
lizard.set_colorkey(colours["transparent"])
pygame.draw.circle(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[7]), treasurecoords[6])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[7]), (treasurecoords[16], treasurecoords[18]), treasurecoords[7])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[22]), (treasurecoords[16], treasurecoords[18]), treasurecoords[6])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[22]), (treasurecoords[16], treasurecoords[25]), treasurecoords[5])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[28]), (treasurecoords[16], treasurecoords[25]), treasurecoords[4])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[28]), (treasurecoords[16], treasurecoords[30]), treasurecoords[3])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[14]), (treasurecoords[24], treasurecoords[13]), treasurecoords[3])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[21]), (treasurecoords[24], treasurecoords[22]), treasurecoords[3])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[14]), (treasurecoords[8], treasurecoords[13]), treasurecoords[3])
pygame.draw.line(lizard, colours["emerald"], (treasurecoords[16], treasurecoords[21]), (treasurecoords[8], treasurecoords[22]), treasurecoords[3])

book = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
book.fill(colours["transparent"])
book.set_colorkey(colours["transparent"])
pygame.draw.polygon(book, colours["brown"], ((treasurecoords[3], treasurecoords[6]), (treasurecoords[3], treasurecoords[25]) ,(treasurecoords[28], treasurecoords[25]), (treasurecoords[28], treasurecoords[6])))
pygame.draw.circle(book, colours["brown"], (treasurecoords[16], treasurecoords[24]), treasurecoords[4])
pygame.draw.polygon(book, colours["creme"], ((treasurecoords[5], treasurecoords[3]), (treasurecoords[5], treasurecoords[22]) ,(treasurecoords[26], treasurecoords[22]), (treasurecoords[26], treasurecoords[3])))

helmet = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
helmet.fill(colours["transparent"])
helmet.set_colorkey(colours["transparent"])
pygame.draw.circle(helmet, colours["grey"], (treasurecoords[16], treasurecoords[13]), treasurecoords[11])
pygame.draw.polygon(helmet, colours["dark"], ((treasurecoords[5], treasurecoords[13]), (treasurecoords[27], treasurecoords[13]), (treasurecoords[27], treasurecoords[28]), (treasurecoords[5], treasurecoords[28])))
pygame.draw.polygon(helmet, colours["grey"], ((treasurecoords[5], treasurecoords[13]), (treasurecoords[7], treasurecoords[13]), (treasurecoords[7], treasurecoords[28]), (treasurecoords[5], treasurecoords[28])))
pygame.draw.polygon(helmet, colours["grey"], ((treasurecoords[25], treasurecoords[13]), (treasurecoords[27], treasurecoords[13]), (treasurecoords[27], treasurecoords[28]), (treasurecoords[25], treasurecoords[28])))
pygame.draw.polygon(helmet, colours["grey"], ((treasurecoords[14], treasurecoords[13]), (treasurecoords[18], treasurecoords[13]), (treasurecoords[18], treasurecoords[23]), (treasurecoords[14], treasurecoords[23])))

spider = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
spider.fill(colours["transparent"])
spider.set_colorkey(colours["transparent"])
pygame.draw.circle(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), treasurecoords[8])
pygame.draw.circle(spider, colours["dark"], (treasurecoords[16], treasurecoords[10]), treasurecoords[4])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[26], treasurecoords[4]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[28], treasurecoords[9]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[26], treasurecoords[27]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[28], treasurecoords[22]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[5], treasurecoords[4]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[3], treasurecoords[9]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[5], treasurecoords[27]), treasurecoords[2])
pygame.draw.line(spider, colours["dark"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[3], treasurecoords[22]), treasurecoords[2])

gold = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
gold.fill(colours["transparent"])
gold.set_colorkey(colours["transparent"])
pygame.draw.circle(gold, colours["rust"], (treasurecoords[16], treasurecoords[16]), treasurecoords[12])
pygame.draw.circle(gold, colours["gold"], (treasurecoords[16], treasurecoords[16]), treasurecoords[9])

dragon = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
dragon.fill(colours["transparent"])
dragon.set_colorkey(colours["transparent"])
pygame.draw.polygon(dragon, colours["rust"], ((treasurecoords[2], treasurecoords[2]), (treasurecoords[16], treasurecoords[16]), (treasurecoords[4], treasurecoords[16])))
pygame.draw.polygon(dragon, colours["rust"], ((treasurecoords[29], treasurecoords[2]), (treasurecoords[16], treasurecoords[16]), (treasurecoords[27], treasurecoords[16])))
pygame.draw.polygon(dragon, colours["dark"], ((treasurecoords[3], treasurecoords[14]), (treasurecoords[29], treasurecoords[14]), (treasurecoords[21], treasurecoords[28]), (treasurecoords[11], treasurecoords[28])))
pygame.draw.polygon(dragon, colours["emerald"], ((treasurecoords[8], treasurecoords[18]), (treasurecoords[24], treasurecoords[18]), (treasurecoords[21], treasurecoords[28]), (treasurecoords[11], treasurecoords[28])))
pygame.draw.circle(dragon, colours["emerald"], (treasurecoords[10], treasurecoords[14]), treasurecoords[8])
pygame.draw.circle(dragon, colours["emerald"], (treasurecoords[23], treasurecoords[14]), treasurecoords[8])
pygame.draw.circle(dragon, colours["offwhite"], (treasurecoords[10], treasurecoords[14]), treasurecoords[6])
pygame.draw.circle(dragon, colours["offwhite"], (treasurecoords[23], treasurecoords[14]), treasurecoords[6])
pygame.draw.circle(dragon, colours["dark"], (treasurecoords[12], treasurecoords[15]), treasurecoords[3])
pygame.draw.circle(dragon, colours["dark"], (treasurecoords[21], treasurecoords[15]), treasurecoords[3])
pygame.draw.circle(dragon, colours["emerald"], (treasurecoords[12], treasurecoords[18]), treasurecoords[4])
pygame.draw.circle(dragon, colours["emerald"], (treasurecoords[21], treasurecoords[18]), treasurecoords[4])
pygame.draw.circle(dragon, colours["dark"], (treasurecoords[12], treasurecoords[18]), treasurecoords[2])
pygame.draw.circle(dragon, colours["dark"], (treasurecoords[21], treasurecoords[18]), treasurecoords[2])

beatle = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
beatle.fill(colours["transparent"])
beatle.set_colorkey(colours["transparent"])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[16]), (treasurecoords[27], treasurecoords[14]), treasurecoords[2])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[28], treasurecoords[20]), treasurecoords[2])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[24]), (treasurecoords[26], treasurecoords[26]), treasurecoords[2])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[16]), (treasurecoords[4], treasurecoords[14]), treasurecoords[2])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[20]), (treasurecoords[3], treasurecoords[20]), treasurecoords[2])
pygame.draw.line(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[24]), (treasurecoords[5], treasurecoords[26]), treasurecoords[2])
pygame.draw.circle(beatle, colours["sapphire"], (treasurecoords[16], treasurecoords[20]), treasurecoords[8])
pygame.draw.polygon(beatle, colours["sapphire"], ((treasurecoords[16], treasurecoords[20]), (treasurecoords[10], treasurecoords[3]), (treasurecoords[8], treasurecoords[20])))
pygame.draw.polygon(beatle, colours["sapphire"], ((treasurecoords[16], treasurecoords[20]), (treasurecoords[22], treasurecoords[3]), (treasurecoords[23], treasurecoords[20])))

princess = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
princess.fill(colours["transparent"])
princess.set_colorkey(colours["transparent"])
pygame.draw.polygon(princess, colours["gold"], ((treasurecoords[6], treasurecoords[30]), (treasurecoords[25], treasurecoords[30]), (treasurecoords[24], treasurecoords[16]), (treasurecoords[7], treasurecoords[16])))
pygame.draw.circle(princess, colours["creme"], (treasurecoords[16], treasurecoords[20]), treasurecoords[9])
pygame.draw.polygon(princess, colours["pink"], ((treasurecoords[24], treasurecoords[16]), (treasurecoords[7], treasurecoords[16]), (treasurecoords[16], treasurecoords[2])))

dwarf = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
dwarf.fill(colours["transparent"])
dwarf.set_colorkey(colours["transparent"])
pygame.draw.circle(dwarf, colours["dark"], (treasurecoords[16], treasurecoords[10]), treasurecoords[8])
pygame.draw.line(dwarf, colours["brown"], (treasurecoords[16], treasurecoords[15]), (treasurecoords[27], treasurecoords[19]), treasurecoords[5])
pygame.draw.circle(dwarf, colours["creme"], (treasurecoords[27], treasurecoords[19]), treasurecoords[3])
pygame.draw.line(dwarf, colours["brown"], (treasurecoords[16], treasurecoords[15]), (treasurecoords[5], treasurecoords[19]), treasurecoords[5])
pygame.draw.circle(dwarf, colours["creme"], (treasurecoords[5], treasurecoords[19]), treasurecoords[3])
pygame.draw.line(dwarf, colours["dark"], (treasurecoords[20], treasurecoords[15]), (treasurecoords[20], treasurecoords[29]), treasurecoords[5])
pygame.draw.line(dwarf, colours["dark"], (treasurecoords[12], treasurecoords[15]), (treasurecoords[12], treasurecoords[29]), treasurecoords[5])
pygame.draw.circle(dwarf, colours["brown"], (treasurecoords[16], treasurecoords[20]), treasurecoords[8])
pygame.draw.circle(dwarf, colours["creme"], (treasurecoords[16], treasurecoords[10]), treasurecoords[6])

treasure = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
treasure.fill(colours["transparent"])
treasure.set_colorkey(colours["transparent"])
pygame.draw.polygon(treasure, colours["brown"], ((treasurecoords[5], treasurecoords[5]), (treasurecoords[5], treasurecoords[26]) ,(treasurecoords[26], treasurecoords[26]), (treasurecoords[26], treasurecoords[5])))
pygame.draw.polygon(treasure, colours["gold"], ((treasurecoords[5], treasurecoords[5]), (treasurecoords[5], treasurecoords[26]) ,(treasurecoords[26], treasurecoords[26]), (treasurecoords[26], treasurecoords[5])), treasurecoords[3])
pygame.draw.line(treasure, colours["gold"], (treasurecoords[5], treasurecoords[16]), (treasurecoords[26], treasurecoords[16]), treasurecoords[3])
pygame.draw.circle(treasure, colours["gold"], (treasurecoords[16], treasurecoords[16]), treasurecoords[4])

rat = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
rat.fill(colours["transparent"])
rat.set_colorkey(colours["transparent"])
pygame.draw.line(rat, colours["dark"], (treasurecoords[22], treasurecoords[24]), (treasurecoords[11], treasurecoords[28]), treasurecoords[2])
pygame.draw.line(rat, colours["dark"], (treasurecoords[21], treasurecoords[28]), (treasurecoords[10], treasurecoords[24]), treasurecoords[2])
pygame.draw.circle(rat, colours["brown"], (treasurecoords[20], treasurecoords[12]), treasurecoords[7])
pygame.draw.circle(rat, colours["dark"], (treasurecoords[20], treasurecoords[12]), treasurecoords[5])
pygame.draw.circle(rat, colours["brown"], (treasurecoords[12], treasurecoords[12]), treasurecoords[7])
pygame.draw.circle(rat, colours["dark"], (treasurecoords[12], treasurecoords[12]), treasurecoords[5])
pygame.draw.circle(rat, colours["brown"], (treasurecoords[16], treasurecoords[16]), treasurecoords[8])
pygame.draw.polygon(rat, colours["brown"], ((treasurecoords[8], treasurecoords[16]), (treasurecoords[23], treasurecoords[16]), (treasurecoords[16], treasurecoords[28])))
pygame.draw.circle(rat, colours["dark"], (treasurecoords[20], treasurecoords[14]), treasurecoords[2])
pygame.draw.circle(rat, colours["dark"], (treasurecoords[12], treasurecoords[14]), treasurecoords[2])

bat = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
bat.fill(colours["transparent"])
bat.set_colorkey(colours["transparent"])
pygame.draw.polygon(bat, colours["dark"], ((treasurecoords[16], treasurecoords[15]), (treasurecoords[28], treasurecoords[11]), (treasurecoords[28], treasurecoords[25]), (treasurecoords[16], treasurecoords[28])))
pygame.draw.circle(bat, colours["transparent"], (treasurecoords[23], treasurecoords[26]), treasurecoords[4])
pygame.draw.polygon(bat, colours["dark"], ((treasurecoords[16], treasurecoords[15]), (treasurecoords[4], treasurecoords[11]), (treasurecoords[4], treasurecoords[25]), (treasurecoords[16], treasurecoords[28])))
pygame.draw.circle(bat, colours["transparent"], (treasurecoords[8], treasurecoords[26]), treasurecoords[4])
pygame.draw.circle(bat, colours["brown"], (treasurecoords[16], treasurecoords[12]), treasurecoords[5])
pygame.draw.polygon(bat, colours["brown"], ((treasurecoords[16], treasurecoords[12]), (treasurecoords[20], treasurecoords[11]),(treasurecoords[18], treasurecoords[3])))
pygame.draw.polygon(bat, colours["brown"], ((treasurecoords[16], treasurecoords[12]), (treasurecoords[12], treasurecoords[11]),(treasurecoords[14], treasurecoords[3])))
pygame.draw.line(bat, colours["brown"], (treasurecoords[16], treasurecoords[14]), (treasurecoords[16], treasurecoords[24]), treasurecoords[5])
pygame.draw.line(bat, colours["brown"], (treasurecoords[16], treasurecoords[19]), (treasurecoords[16], treasurecoords[29]), treasurecoords[3])

owl = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
owl.fill(colours["transparent"])
owl.set_colorkey(colours["transparent"])
pygame.draw.line(owl, colours["dark"], (treasurecoords[20], treasurecoords[24]), (treasurecoords[20], treasurecoords[28]), treasurecoords[3])
pygame.draw.line(owl, colours["dark"], (treasurecoords[12], treasurecoords[24]), (treasurecoords[12], treasurecoords[28]), treasurecoords[3])
pygame.draw.circle(owl, colours["rust"], (treasurecoords[16], treasurecoords[20]), treasurecoords[8])
pygame.draw.circle(owl, colours["brown"], (treasurecoords[12], treasurecoords[12]), treasurecoords[6])
pygame.draw.circle(owl, colours["brown"], (treasurecoords[20], treasurecoords[12]), treasurecoords[6])
pygame.draw.circle(owl, colours["offwhite"], (treasurecoords[12], treasurecoords[12]), treasurecoords[4])
pygame.draw.circle(owl, colours["offwhite"], (treasurecoords[20], treasurecoords[12]), treasurecoords[4])
pygame.draw.circle(owl, colours["dark"], (treasurecoords[12], treasurecoords[12]), treasurecoords[2])
pygame.draw.circle(owl, colours["dark"], (treasurecoords[20], treasurecoords[12]), treasurecoords[2])
pygame.draw.line(owl, colours["brown"], (treasurecoords[24], treasurecoords[16]), (treasurecoords[24], treasurecoords[24]), treasurecoords[3])
pygame.draw.line(owl, colours["brown"], (treasurecoords[8], treasurecoords[16]), (treasurecoords[8], treasurecoords[24]), treasurecoords[3])

compass = pygame.Surface((lengths["treasurespritewidthheight"], lengths["treasurespritewidthheight"]))
compass.fill(colours["transparent"])
compass.set_colorkey(colours["transparent"])
pygame.draw.polygon(compass, colours["brown"], ((treasurecoords[4], treasurecoords[6]), (treasurecoords[6], treasurecoords[4]), (treasurecoords[25], treasurecoords[4]), (treasurecoords[27], treasurecoords[6]), (treasurecoords[27], treasurecoords[25]), (treasurecoords[25], treasurecoords[27]), (treasurecoords[6], treasurecoords[27]), (treasurecoords[4], treasurecoords[25])))
pygame.draw.circle(compass, colours["offwhite"], (treasurecoords[16], treasurecoords[16]), treasurecoords[10])
pygame.draw.line(compass, colours["rust"], (treasurecoords[12], treasurecoords[12]), (treasurecoords[16], treasurecoords[16]), treasurecoords[5])
pygame.draw.line(compass, colours["dark"], (treasurecoords[16], treasurecoords[16]), (treasurecoords[20], treasurecoords[20]), treasurecoords[5])

treasuresprites = {"ring" : ring,
                  "genie" : genie,
                  "crown" : crown,
                  "candle" : candle,
                  "ghost" : ghost,
                  "keys" : keys,
                  "skull" : skull,
                  "moth" : moth,
                  "gem" : gem,
                  "sword" : sword,
                  "lizard" : lizard,
                  "book" : book,
                  "helmet" : helmet,
                  "spider" : spider,
                  "gold" : gold,
                  "dragon" : dragon,
                  "beatle" : beatle,
                  "princess" : princess,
                  "dwarf" : dwarf,
                  "treasure" : treasure,
                  "rat" : rat,
                  "bat" : bat,
                  "owl" : owl,
                  "compass" : compass}

leftbutton = pygame.Surface((lengths["tilesegmentwidthheight"], lengths["tilesegmentwidthheight"]))
leftbutton.fill(colours["sand"])
pygame.draw.line(leftbutton, colours["beige"], 
                 (lengths["tilesegmentwidthheight"] // 6, lengths["tilesegmentwidthheight"] // 2), 
                 (lengths["tilesegmentwidthheight"] - lengths["tilesegmentwidthheight"] // 6, lengths["tilesegmentwidthheight"] // 2), 3)
pygame.draw.polygon(leftbutton, colours["beige"], ((lengths["tilesegmentwidthheight"] // 6, lengths["tilesegmentwidthheight"] // 2), 
                                                   (lengths["tilesegmentwidthheight"] // 2, lengths["tilesegmentwidthheight"] // 6), 
                                                   (lengths["tilesegmentwidthheight"] // 2, lengths["tilesegmentwidthheight"] - lengths["tilesegmentwidthheight"] // 6)))
rightbutton = pygame.transform.flip(leftbutton, True, False)

helpbutton = Card("Help")

screen = pygame.display.set_mode((lengths["screenwidth"], lengths["screenheight"]))
screen.fill(colours["white"])

###     GAME SETUP     ###

menu = Menu()
winscreen = Winscreen()
board = Board()
guide = Guide()
fixed = []
moveable = []

yellowtile = Tile([True, True, False, False], None)
redtile = Tile([True, False, False, True], None)
greentile = Tile([False, True, True, False], None)
bluetile = Tile([False, False, True, True], None)
treasures = ["book", "gold", "compass", "crown", "keys", "skull",
             "ring", "treasure", "gem", "sword", "candle", "helmet",
             "rat", "beatle", "lizard", "moth", "spider", "owl",
             "genie", "ghost", "dragon", "dwarf", "princess", "bat"]

deck = []
for i in range(len(treasures)):
    deck.append(Card(treasures[i]))

fixed.append(yellowtile)
for i in range(2):
    fixed.append(Tile([False, False, False, True], treasures[0]))
    treasures = treasures[1:]
    for j in range(3):
        fixed[-1].rotate("left")
fixed.append(redtile)
for i in range(8):
    fixed.append(Tile([False, False, False, True], treasures[0]))
    treasures = treasures[1:]
    if i == 0 or i == 4 or i == 5:
        for j in range(2):
            fixed[-1].rotate("left")
    elif i == 1:
        for j in range(3):
            fixed[-1].rotate("left")
    elif i == 6:
        fixed[-1].rotate("left")
fixed.append(greentile)
for i in range(2):
    fixed.append(Tile([False, False, False, True], treasures[0]))
    treasures = treasures[1:]
    fixed[-1].rotate("left")
fixed.append(bluetile)

for i in range(10):
    moveable.append(Tile([False, False, True, True], None))
    for j in range(random.randint(0, 3)):
        moveable[-1].rotate("left")
for i in range(6):
    moveable.append(Tile([False, False, True, True], treasures[0]))
    treasures = treasures[1:]
    for j in range(random.randint(0, 3)):
        moveable[-1].rotate("left")
for i in range(12):
    moveable.append(Tile([True, False, True, False], None))
    for j in range(random.randint(0, 3)):
        moveable[-1].rotate("left")
for i in range(6):
    moveable.append(Tile([False, False, False, True], treasures[0]))
    treasures = treasures[1:]
    for j in range(random.randint(0, 3)):
        moveable[-1].rotate("left")

pygame.display.update()

num = 2
flag = "menu"
guideflag = False
while True:
    if flag == "menu":
        screen.blit(menu.sprite, (0, 0))
        if guideflag:
            guide.drawguide(0, i)
        pygame.display.update()
        action = getpygameinput("menu")
        if action == "play":
            flag = "game"
            num = menu.num
        elif action == "guide":
            guideflag = not guideflag
        elif action == "increase":
            if menu.num != 4:
                menu.num += 1
                menu.update()
        elif action == "decrease":
            if menu.num != 1:
                menu.num -= 1
                menu.update()

    if flag == "game":
        random.shuffle(deck)
        playersandpos = createplayers(deck, num)
        players = playersandpos[0]
        playerpos = playersandpos[1]                 

        random.shuffle(moveable)
        outtile = board.generate(fixed, moveable)
        screen.fill(colours["white"])
        board.update()
        for i in range(len(players)):
            players[i].position = playerpos[i]
            players[i].update()

        screen.blit(leftbutton, coords["leftbutton"])
        screen.blit(rightbutton, coords["rightbutton"])
        screen.blit(outtile.sprite, coords["outtile"])
        screen.blit(helpbutton.sprite, coords["helpbutton"])
        win = False
        while not win:
            for i in range(len(players)):
                card = Card(None)
                screen.blit(card.sprite, coords["card"])
                if guideflag:
                    guide.drawguide(1, i)
                pygame.display.update()
                while True:
                    inp = getpygameinput("game")
                    if inp[0] == "help":
                        guideflag = True
                        guide.drawguide(1, i)
                        pygame.display.update()
                    elif inp:
                        break
                
                card = Card(players[i].cards[0].item)
                screen.blit(card.sprite, coords["card"])
                if guideflag:
                    guide.drawguide(2, i)
                pygame.display.update()
                
                while True:
                    inp = getpygameinput("game")
                    if inp[0] == "tile":
                        tileplayers = board.move(inp[1], outtile, playerpos)
                        outtile = tileplayers[0]
                        playerpos = tileplayers[1]
                        for j in range(len(playerpos)):
                            players[j].position = playerpos[j]
                        screen.blit(outtile.sprite, coords["outtile"])
                        pygame.display.update()
                        break
                    elif inp[0] == "button":
                        outtile.rotate(inp[1])
                        screen.blit(outtile.sprite, coords["outtile"])
                        pygame.display.update()
                    elif inp[0] == "help":
                        guideflag = True
                        guide.drawguide(2, i)
                        pygame.display.update()

                if guideflag:
                    guide.drawguide(3, i)
                    
                board.update()
                for j in range(len(players)):
                    players[j].update()
                if guideflag:
                    guide.drawguide(4, i)
                pygame.display.update()
                while True:
                    inp = getpygameinput("game")
                    if inp[0] == "player":
                        if inp[1] in board.traverse(players[i].position, None, [players[i].position]):
                            players[i].move(inp[1])
                            playerpos = []
                            for j in range(len(players)):
                                playerpos.append(players[j].position)
                            break
                    elif inp[0] == "button":
                        outtile.rotate(inp[1])
                        screen.blit(outtile.sprite, coords["outtile"])
                        pygame.display.update()
                    elif inp[0] == "help":
                        guideflag = True
                        guide.drawguide(4, i)
                        pygame.display.update()
                board.update()
                for j in range(len(players)):
                    players[j].update()
                pygame.display.update()
                if board.grid[players[i].position[0]][players[i].position[1]].item == players[i].cards[0].item:
                    players[i].treasurefound()

                guideflag = False
                updatescore(i)

                players[i].cards = []

                if len(players[i].cards) == 0:
                        win = True
                        flag = "win"
                        winner = players[i]
                        break

        if flag == "win":
            winscreen.draw(winner)
            pygame.display.update()
            while True:
                    inp = getpygameinput("game")
                    if inp:
                        break
            flag = "menu"
