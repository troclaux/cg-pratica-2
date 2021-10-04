import math
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

# para poder carregar uma malha .obj:
loadPrcFileData("","load-file-type p3assimp")

# deativar caching (para que o panda3D não use dados "velhos"):
cache = BamCache.get_global_ptr()
cache.set_active(False)


class MeuApp(ShowBase):
    def __init__(self):
        '''Abre a janela, cria um gráfo de cena e prepara tudo que é preciso
        para renderizar essa cena na janela. Define a luz da cena, chama um
        método que carrega malhas em formato .obj e mapea texturas nelas. Chama 
        também um método que define a câmera e o movimento/setting dela.'''
        ShowBase.__init__(self)
        self.carregarModelos()

        # definir luz e sombra:
        alight = AmbientLight('Ambient')
        alight.setColor((0.4, 0.4, 0.4, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        
        plight = PointLight('plight')
        plight.setColor((0.6, 0.6, 0.6, 1))
        plight.setShadowCaster(True, 2048, 2048)
        self.render.setShaderAuto()
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(2, 6, 3)
        self.render.setLight(plnp)
    
        # desativar trackball controle de camera:
        base.disableMouse()
        # chamar o método dollyZoomTask cada frame:
        self.taskMgr.add(self.dollyZoomTask, "DollyZoomTask")


        
    ##========== Método que carrega as malhas ========== 
    def carregarModelos(self):
        '''Carrega malhas em formato .obj e mapea texturas nelas. Especifica
        a posição, escalonamento e a orientação dos modelos. Coloca os modelos
        no grafo de cena usando o método reparentTo.'''

        self.fundo = self.loader.loadModel("esquina_tex.obj")
        tex = loader.loadTexture('esquina.png')
        self.fundo.setTexture(tex,1)
        self.fundo.reparentTo(self.render) # fazendo a malha visível

        self.bob = self.loader.loadModel("bob190k_tex.obj")
        tex = loader.loadTexture('bob_diffuse.png')
        self.bob.setTexture(tex,1)
        self.bob.setScale(1, 1, 1.5) # escalonamento X, Y, Z 
        self.bob.setHpr(180,0,0) # rotacao em volta de Z, X, Y
        self.bob.setPos(0,3,0) # posicao (X,Y,Z)
        self.bob.reparentTo(self.render)
 
        self.spot1 = self.loader.loadModel("spot190k_tex.obj")
        tex = loader.loadTexture('spot_blue.png')
        self.spot1.setTexture(tex,1)
        self.spot1.setScale(1.2, 1.2, 1.2) 
        self.spot1.setHpr(77, 23, 111)
        self.spot1.setPos(0, 0, 4)
        self.spot1.reparentTo(self.render)

        self.spot2 = self.loader.loadModel('spot190k_tex.obj')
        tex = loader.loadTexture('spot_red.png')
        self.spot2.setTexture(tex,1)
        self.spot2.setScale(2, 2, 2)
        self.spot2.setHpr(30, 0, 0)
        self.spot2.setPos(3, -1, 0)
        self.spot2.reparentTo(self.render)

        self.spot3 = self.loader.loadModel('spot190k_tex.obj')        
        tex = loader.loadTexture('spot_green.png')
        self.spot3.setTexture(tex,1)
        self.spot3.setPos(-2,-2,0)
        self.spot3.reparentTo(self.render)

        self.wood_table = self.loader.loadModel("wood_table.obj")
        tex = loader.loadTexture('wood_table_texture.jpg')
        self.wood_table.setTexture(tex, 1)
        self.wood_table.setPos(0, 0.5, 0)
        self.wood_table.reparentTo(self.render)
        self.wood_table.setHpr(0, 90, 90)
        self.wood_table.setScale(3, 3, 3)

        self.shovel = self.loader.loadModel("shovel.obj")
        tex = loader.loadTexture('shovel_texture.png')
        self.shovel.setTexture(tex, 1)
        self.shovel.setPos(1, 0.5, 2)
        self.shovel.reparentTo(self.render)
        self.shovel.setHpr(0, 0, 0)
        #self.shovel.setScale(2, 2, 3)  # escalonamento X, Y, Z

        self.lamp_post = self.loader.loadModel("lamp_post.obj")
        tex = loader.loadTexture('lamp_post_texture.png')
        self.lamp_post.setTexture(tex, 1)
        self.lamp_post.setPos(-3, 0.5, 0)
        self.lamp_post.reparentTo(self.render)
        self.lamp_post.setHpr(90, 90, 0)
        self.lamp_post.setScale(0.5, 0.5, 0.5)  # escalonamento X, Y, Z

    ##========== Método que define o movimento de camera ========== 
    def dollyZoomTask(self, tarefa):
        '''O movimento da câmera nessa cena tem como objetivo dar o foco no bob e na mesa, além disso a posição inicial permite que a câmera mostre as sombras dos modelos. A câmera começa com um ponto de vista top-down da cena e se aproxima do chão enquanto simultaneamente muda o FOV. Depois ela percorre o caminho inverso enquanto volta pro FOV original. A câmera vai continuar percorrendo esse trajeto repetidamente.'''
        # math.sin é usada para criar um movimento periódico
        #tarefa.time retorna o tempo que se passou em segundos, a funcao

        largura = 4
        FOV = 40 + 20 * math.sin(math.pi * tarefa.time/2)
        distance = largura/(2*math.tan(0.5*FOV/180*math.pi))
        self.camera.lookAt(0, -1, -3)
        self.camera.setPos(0, distance + 2, 10)
        base.camLens.setFov(FOV)
        return tarefa.cont


aula4 = MeuApp()
# última linha: metódo run renderiza a janela e trata as background tarefas:
aula4.run()
