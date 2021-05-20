import pygame
import sys
import random;

window_height = 800
window_width = 800

background = [0, 0, 0] #Black

blocks = [(48, 116, 253), (230, 204, 108)] #Ocean (Blue), Sand (Orange?)

cellSize = 5 #Size of the grid cell
percentage = 60 #Amount of ocean in the grid. (60% Generates cool caves at 5 cell size)

baseCells = [[0 for x in range(window_width)] for y in range(window_width)] #Store grid cell colors

mode = "Normal" #Normal, Caves/Islands.

started = False
showSelectionMenu = False

def main():
    global screen, started, mode, showSelectionMenu, cellSize
    pygame.init()

    screen = pygame.display.set_mode((window_width, window_height))

    #Setup Fonts
    smallFont = pygame.font.SysFont('arial', 20, bold = True)
    font = pygame.font.SysFont('arial', 38)

    #Menu Texts
    clickToStart = font.render('Click on the screen or on the red dot', True, [0, 0, 0])
    normalModeText = font.render('Normal', True, [0, 0, 0])
    islandModeText = font.render('Caves/Islands', True, [0, 0, 0])

    #Menu Buttons
    selectionButton = pygame.Rect(10, 10, 20, 20)
    normalModeButton = pygame.Rect(10, 38, 220, 40)
    islandModeButton = pygame.Rect(10, 86, 220, 40)

    sizesButtons = []
    sizesText = []
    for x in range(11): #Setup cell size menu buttons
        sizesButtons.append(pygame.Rect(10 + 22 * x, 134, 20, 20))
        if(x * 5 == 0):
            sizesText.append(smallFont.render(str(1), True, [0, 0, 0]))
        else:
            sizesText.append(smallFont.render(str(x * 5), True, [0, 0, 0]))

    pygame.display.set_caption('Cellular Automata')

    screen.fill(background)

    definebaseCells()

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (selectionButton.collidepoint(event.pos)):
                    showSelectionMenu = not showSelectionMenu
                elif (showSelectionMenu and normalModeButton.collidepoint(event.pos)):
                    showSelectionMenu = False
                    mode = "Normal"
                    definebaseCells()
                elif (showSelectionMenu and islandModeButton.collidepoint(event.pos)):
                    showSelectionMenu = False
                    mode = "Caves/Islands"
                    definebaseCells()
                else:
                    if(not started):
                        started = True

                    if(showSelectionMenu):
                        for x in range(len(sizesButtons)):
                            if(sizesButtons[x].collidepoint(event.pos)):
                                showSelectionMenu = False
                                if(x * 5 == 0):
                                    cellSize = 1
                                else:
                                    cellSize = x * 5
                                definebaseCells()
                                continue

                    cellularAutomata()
        
        pygame.draw.rect(screen, [250, 70, 60], selectionButton)
        modeText = smallFont.render("{} - {}".format(mode, cellSize), True, [0, 0, 0])
        screen.blit(modeText, [32, 10])

        if(not started):
            screen.blit(clickToStart,(window_width / 2.0 - 260, window_height / 2.0 - 80))

        if(showSelectionMenu): #Render menu when active
            pygame.draw.rect(screen, [250, 70, 60], normalModeButton)
            screen.blit(normalModeText, [10, 38])

            pygame.draw.rect(screen, [250, 70, 60], islandModeButton)
            screen.blit(islandModeText, [10, 86])

            for x in range(len(sizesButtons)):
                pygame.draw.rect(screen, [250, 70, 60], sizesButtons[x])
                screen.blit(sizesText[x], [10 + 22 * x, 134])

        pygame.display.update()

def definebaseCells(): #Define an initial random type of block to each cell.
    for x in range(0, window_width, cellSize):
        for y in range(0, window_height, cellSize):
            p = random.randint(0, 100)
            if(p < percentage):
                baseCells[x][y] = blocks[0]
            else:
                baseCells[x][y] = blocks[1]

def drawGrid():
    for x in range(0, window_width, cellSize):
        for y in range(0, window_height, cellSize):
            cell = pygame.Rect(x, y, cellSize, cellSize)
            pygame.draw.rect(screen, baseCells[x][y], cell)

def cellularAutomata():
    baseCellsHolder = [[0 for x in range(window_width)] for y in range(window_width)] #Holder for the cellular automata changes.

    for x in range(0, window_width, cellSize):
        for y in range(0, window_height, cellSize):

            #Check Neighbours

            count = 0 #Amount of ocean neighbours.

            #Rules for Normal:
            #A cell needs to have 3 ocean neighbours to become a sand, if not, it becomes an ocean.
            #Outside of the grid cells (Corner) are counted as ocean.

            #Rules for Caves/Islands:
            #A cell needs to have 4 or less ocean neighbours to become a sand, if not, it becomes an ocean.
            #Outside of the grid cells (Corner) are counted as ocean.

            #Left
            if(x - cellSize >= 0):
                if(baseCells[x - cellSize][y] == blocks[0]):
                    count += 1
            else:
                count += 1

            #Right
            if(x + cellSize < window_width):
                if(baseCells[x + cellSize][y] == blocks[0]):
                    count += 1
            else:
                count += 1
            
            #Up
            if(y - cellSize >= 0):
                if(baseCells[x][y - cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1
            
            #Up-Left
            if(x - cellSize >= 0 and y - cellSize >= 0):
                if(baseCells[x - cellSize][y - cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1
            
            #Up-Right
            if(x + cellSize < window_width and y - cellSize >= 0):
                if(baseCells[x + cellSize][y - cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1

            #Bottom
            if(y + cellSize < window_height):
                if(baseCells[x][y + cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1
            
            #Bottom-Left
            if(x - cellSize >= 0 and y + cellSize < window_height):
                if(baseCells[x - cellSize][y + cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1

            #Bottom-Right
            if(x + cellSize < window_width and y + cellSize < window_height):
                if(baseCells[x + cellSize][y + cellSize] == blocks[0]):
                    count += 1
            else:
                count += 1
            
            if mode == "Normal":
                if(8 - count == 3): #8 - Total Ocean Neighbours = Total Sand Neighbours
                    baseCellsHolder[x][y] = blocks[1] #Sand
                else:
                    baseCellsHolder[x][y] = blocks[0] #Ocean

            elif mode == "Caves/Islands":
                if(count <= 4):
                    baseCellsHolder[x][y] = blocks[1] #Sand
                else:
                    baseCellsHolder[x][y] = blocks[0] #Ocean
            
    
    for x in range(0, window_width, cellSize): #Apply the changes from the holder to the grid.
        for y in range(0, window_height, cellSize):
            baseCells[x][y] = baseCellsHolder[x][y]

main();