import pygame

class showInventary():
    def __init__(self,inventory,screen):
        self.active = False
        self.showArtefactActive = False
        self.text_font = pygame.font.SysFont("Arial", 50)
        self.allCases = []

        self.text_font_inventaire_titre = pygame.font.Font("../Design/gabriola.ttf", 50)
        self.text_font_inventaire_titre.bold = True
        self.text_font_inventaire_content = pygame.font.Font("../Design/gabriola.ttf", 30)

        self.inventoryDesign = pygame.image.load("../Design/Inventaire_Artefacts.png")
        self.inventoryDesign = pygame.transform.scale(self.inventoryDesign,(self.inventoryDesign.get_width()*1.5,self.inventoryDesign.get_height()*1.5))
        self.inventoryShowArtefactDesign = pygame.image.load("../Design/Interface_Artefacts.png")
        self.inventoryShowArtefactDesign = pygame.transform.scale(self.inventoryShowArtefactDesign, (self.inventoryShowArtefactDesign.get_width() * 1.5, self.inventoryShowArtefactDesign.get_height() * 1.5))

        for i,artefact in enumerate(inventory):
            case = pygame.Rect(self.inventoryDesign.get_rect().centerx - 100 + (
                        (self.inventoryDesign.get_width() // 4) * (i % 3) + 65 * (i % 3)-100),
                               self.inventoryDesign.get_height() // 3 * 1.45 + (self.inventoryDesign.get_height() // 4) * (i // 3) + 30 * (i // 3)-100,
                               (self.inventoryDesign.get_width() // 4),
                               (self.inventoryDesign.get_height() // 4))
            self.allCases.append(case)

    def DisplayInventory(self,inventory,screen):
        screen.display.fill((52, 78, 91))
        screen.display.blit(self.inventoryDesign,(100,100))
        font = self.text_font_inventaire_titre.render("INVENTAIRE", True, (255,255,255))
        screen.display.blit(font, (screen.display.get_width()//3*2,50))

        #### Mettre AllCase pour les collisions
        for i,artefact in enumerate(inventory):
            case = pygame.Rect(self.inventoryDesign.get_rect().centerx -100 + ((self.inventoryDesign.get_width() // 4)*(i%3) + 65 *(i%3)),
                self.inventoryDesign.get_height()//3 *1.45 + (self.inventoryDesign.get_height()//4)*(i//3) + 30*(i//3),
                (self.inventoryDesign.get_width() // 4),
                (self.inventoryDesign.get_height() // 4))
            if not inventory[i] == "":
                image = pygame.image.load(f"../Design/{inventory[i]}.png")
                image = pygame.transform.scale(image,(100,100))
                screen.display.blit(image,(self.allCases[i].centerx-(self.allCases[i].centerx - self.allCases[i].x)+ 20,self.allCases[i].centery-(self.allCases[i].centery - self.allCases[i].y)+10))
    def showArtefact(self,artefactName,screen,jsonfile,font1,font2):
        self.showArtefactActive = True
        screen.display.blit(self.inventoryShowArtefactDesign,(400,250))
        image = pygame.image.load(f"../Design/{artefactName}.png")
        screen.display.blit(pygame.transform.scale(image,(image.get_width()*1.5,image.get_height()*1.5)),(self.inventoryShowArtefactDesign.get_rect().centerx-100,self.inventoryShowArtefactDesign.get_rect().centery+350))
        for i in range(0,9):
            if jsonfile["artefact"][i]["name"] == artefactName:
                font1 = font1.render(str(jsonfile["artefact"][i]["titre"]),True,(0,0,0))
                screen.display.blit(font1,(self.inventoryShowArtefactDesign.get_rect().centerx+400,self.inventoryShowArtefactDesign.get_rect().centery-55))
                font2 = font2.render(str(jsonfile["artefact"][i]["description"]), True, (0, 0, 0))
                screen.display.blit(font2, (self.inventoryShowArtefactDesign.get_rect().centerx+400,self.inventoryShowArtefactDesign.get_rect().centery))
    def ClickItem(self,event,inventaire,screen,jsonfile):
        for i,case in enumerate(self.allCases):
            if not inventaire[i] == "":
                if event.pos[0] < case.right and event.pos[0] > case.left and event.pos[1] < case.bottom and event.pos[1] > case.top:
                    self.active = False
                    self.showArtefact(inventaire[i],screen,jsonfile,self.text_font_inventaire_titre,self.text_font_inventaire_content)


