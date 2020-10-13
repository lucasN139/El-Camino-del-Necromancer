import pygame,sys,os,time,math,random
from pygame.locals import *
from archivo_niveles import *

from pygame import mixer

pygame.init()
fuente = pygame.font.SysFont("Arial", 35)
fuente2 = pygame.font.SysFont("Arial", 25)

screen = pygame.display.set_mode((940, 380))
pygame.display.set_caption("Juego de Plataformas")

clock = pygame.time.Clock()

modo=""
#admin

mixer.music.load("sonidos/Battle-of-the-Ancients.wav")
mixer.music.play(-1)

class Botones:
	def __init__(self, color, width, height, posx, posy):
		self.color = color
		self.width = width
		self.height = height
		self.posx = posx
		self.posy = posy


	def click(self, pos):
	#Pos posicion del mouse o tupla de x,y coordenadas
		if pos[0] > self.posx and pos[0] < self.posx + self.width:
			if pos[1] > self.posy and pos[1] < self.posy + self.height:
				return True
		return False

class propiedades:
	def __init__(self, posx, posy, width, height,vida):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.hitbox=pygame.Rect(self.posx, self.posy, self.width, self.height)

		self.vida=vida
		
		self.tiempo_pasado=0
		self.num_animacion=0
		self.direccion=""
		self.direcciony=""
		self.seleccionado=0

		self.hitbox_hechizo=pygame.Rect(self.posx, self.posy-5, 24, 14)
		self.direccion_hechizo=""
		self.hechizo_lanzado=False
		self.tiempo_hechizo=0

		self.dragon_hechizo=[]
		self.siendo_atacado=False

	def imagenes(self,imagen):
		self.imagen=[]
		self.imagen=imagen

	def hechizo(self,seleccionado):
		global daño_recibido

		if seleccionado==1: 
			#activa
			if tecla[pygame.K_SPACE] and self.hechizo_lanzado==False:
				hechizo_sonido = mixer.Sound("sonidos/Fireball.wav")
				hechizo_sonido.play()
				self.hitbox_hechizo.x=self.posx
				self.hitbox_hechizo.y=self.posy
				self.hechizo_lanzado=True
				self.direccion_hechizo=self.direccion

			#mantiene
			if self.hechizo_lanzado==True:
				#pygame.draw.rect(screen, (255,0,0), (self.hitbox_hechizo.x,self.hitbox_hechizo.y,self.hitbox_hechizo.width,self.hitbox_hechizo.height))
				if self.direccion_hechizo=="derecha" or self.direccion_hechizo=="":
					self.hitbox_hechizo.x+=7
					screen.blit(pygame.image.load("imagenes/jugador/ataqued.png"),(self.hitbox_hechizo.x,self.hitbox_hechizo.y))

				elif self.direccion_hechizo=="izquierda":
					self.hitbox_hechizo.x-=7
					screen.blit(pygame.image.load("imagenes/jugador/ataquei.png"),(self.hitbox_hechizo.x,self.hitbox_hechizo.y))

				self.tiempo_hechizo+=1
				if self.tiempo_hechizo>=20:
					self.hechizo_lanzado=False
					self.tiempo_hechizo=0
					self.hitbox_hechizo.x=0
					self.hitbox_hechizo.y=0

				for muro in muros_marrones:
					if self.hitbox_hechizo.colliderect(muro.rect)==True:
						self.hechizo_lanzado=False
						self.tiempo_hechizo=0
						self.hitbox_hechizo.x=0
						self.hitbox_hechizo.y=0
				for muro in muros_negros:
					if self.hitbox_hechizo.colliderect(muro.rect)==True:
						self.hechizo_lanzado=False
						self.tiempo_hechizo=0
						self.hitbox_hechizo.x=0
						self.hitbox_hechizo.y=0
				for muro in muros_verdes:
					if self.hitbox_hechizo.colliderect(muro.rect)==True:
						self.hechizo_lanzado=False
						self.tiempo_hechizo=0
						self.hitbox_hechizo.x=0
						self.hitbox_hechizo.y=0
				for muro in piedras:
					if self.hitbox_hechizo.colliderect(muro.rect)==True:
						self.hechizo_lanzado=False
						self.tiempo_hechizo=0
						self.hitbox_hechizo.x=0
						self.hitbox_hechizo.y=0

		elif seleccionado==2:
			for x in self.dragon_hechizo:
				#pygame.draw.rect(screen, (255,0,0), (x.hitbox_hechizo.x,x.hitbox_hechizo.y,x.hitbox_hechizo.width,x.hitbox_hechizo.height))

				if x.vida==1:
					x.hitbox_hechizo.width=x.hitbox_hechizo.width+25
					x.hitbox_hechizo.height=x.hitbox_hechizo.height+5
					x.hechizo_lanzado=True
					x.vida=0
				if self.direccion=="derecha":
					x.direccion_hechizo="derecha"
				else:
					x.direccion_hechizo="izquierda"

				if x.direccion_hechizo=="derecha" and x.hechizo_lanzado==True:
					x.hitbox_hechizo.x+=7
					screen.blit(pygame.image.load("imagenes/dragon/Fire_Attack1d.png"),(x.hitbox_hechizo.x,x.hitbox_hechizo.y))

				elif x.direccion_hechizo=="izquierda" and x.hechizo_lanzado==True:
					x.hitbox_hechizo.x-=7
					screen.blit(pygame.image.load("imagenes/dragon/Fire_Attack1i.png"),(x.hitbox_hechizo.x,x.hitbox_hechizo.y))


				for muro in muros_marrones:
					if x.hitbox_hechizo.colliderect(muro.rect)==True:
						self.dragon_hechizo.remove(x)

				for muro in muros_negros:
					if x.hitbox_hechizo.colliderect(muro.rect)==True:
						self.dragon_hechizo.remove(x)

				for muro in muros_verdes:
					if x.hitbox_hechizo.colliderect(muro.rect)==True:
						self.dragon_hechizo.remove(x)

				for muro in piedras:
					if x.hitbox_hechizo.colliderect(muro.rect)==True:
						self.dragon_hechizo.remove(x)

				if x.hitbox_hechizo.colliderect(heroe_jugador.hitbox_hechizo)==True:
						self.dragon_hechizo.remove(x)

				if x.hitbox_hechizo.colliderect(heroe_jugador.hitbox)==True:
					daño_recibido=True




	def animar(self):
		global tecla,daño_recibido
		self.tiempo_pasado+=1

		screen.blit(self.imagen[self.num_animacion],(self.posx,self.posy))
		tecla= pygame.key.get_pressed()

		if daño_recibido==True and self.num_animacion<13:
			self.num_animacion=13
		if daño_recibido==True:
			if self.num_animacion<19:
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0

		elif tecla[pygame.K_RIGHT] or tecla[pygame.K_d] :

			self.direccion="derecha"
			if self.num_animacion<=5:
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0
			else:
				self.num_animacion=1

		elif tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
			self.direccion="izquierda"
			if self.num_animacion<=12 and self.num_animacion>=8:
				screen.blit(self.imagen[self.num_animacion],(self.posx,self.posy))
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0
			else:
				self.num_animacion=8
		else:
			if self.direccion=="izquierda":
				self.num_animacion=7
			else:
				self.num_animacion=0

#-------------------------
	def animar_lizard(self):
		self.tiempo_pasado+=1
		if self.vida>0 or self.vida<=0 and self.num_animacion>=13 and self.num_animacion<18:
			screen.blit(lizard_imagenes[self.num_animacion],(self.hitbox.x,self.hitbox.y))
			if self.vida<=0:
				dragon_sonido = mixer.Sound("sonidos/lizard_muerte.wav")
				dragon_sonido.play()

		if self.vida <= 0:
			if self.num_animacion<13:
				self.num_animacion=13
			if self.num_animacion>=13 and self.num_animacion<18:
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0
		else:

			if self.direccion=="derecha":
				if self.num_animacion<5:
					if self.tiempo_pasado>=4:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
				else:
					self.num_animacion=0
			elif self.direccion=="izquierda":
				if self.num_animacion<10 and self.num_animacion>=7:
					if self.tiempo_pasado>=4:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
				else:
					self.num_animacion=7

	def animar_calavera(self):
		self.tiempo_pasado+=1
		screen.blit(calavera_imagenes[self.num_animacion],(self.hitbox.x,self.hitbox.y))
		if self.direccion=="derecha":
			if self.num_animacion<9:
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0
			else:
				self.num_animacion=0
		elif self.direccion=="izquierda":
			if self.num_animacion>10 and self.num_animacion<18:
				if self.tiempo_pasado>=4:
					self.num_animacion=self.num_animacion+1
					self.tiempo_pasado=0
			else:
				self.num_animacion=10

	def animar_dragon(self):
		self.tiempo_pasado+=1
		if self.vida>0 or self.vida<=0 and self.num_animacion>=8 and self.num_animacion<12 or self.vida<=0 and self.num_animacion>=23 and self.num_animacion<28:
			screen.blit(dragon_imagenes[self.num_animacion],(self.hitbox.x,self.hitbox.y))
			if self.vida<=0:
				dragon_sonido = mixer.Sound("sonidos/dragon_muerte.wav")
				dragon_sonido.play()


		if self.direccion=="derecha":
			if self.vida>=0:
				if self.num_animacion<6:
					if self.tiempo_pasado>=8:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
						#if self.siendo_atacado==True:
							#screen.blit(dragon_imagenes[7],(self.hitbox.x,self.hitbox.y))
							#self.siendo_atacado=False

						if self.num_animacion>=6:
							self.dragon_hechizo.append(propiedades(self.posx+45,self.posy+15,self.width,self.height,1))
							self.direccion_hechizo=self.direccion
				else:
					self.num_animacion=0

			else:
				if self.num_animacion<8:
					self.num_animacion=8
				if self.num_animacion>=8 and self.num_animacion<12:
					if self.tiempo_pasado>=4:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
				else:
					self.num_animacion==8


		elif self.direccion=="izquierda":
			if self.vida>=0:
				if self.num_animacion>=16 and self.num_animacion<21:
					if self.tiempo_pasado>=8:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
						#if self.siendo_atacado==True:
							#screen.blit(dragon_imagenes[7],(self.hitbox.x,self.hitbox.y))
							#self.siendo_atacado=False

						if self.num_animacion>=21:
							self.dragon_hechizo.append(propiedades(self.posx+25,self.posy+15,self.width,self.height,1))
							self.direccion_hechizo=self.direccion
				else:
					self.num_animacion=16

			else:
				if self.num_animacion<23:
					self.num_animacion=23
				if self.num_animacion>=23 and self.num_animacion<28:
					if self.tiempo_pasado>=4:
						self.num_animacion=self.num_animacion+1
						self.tiempo_pasado=0
				else:
					self.num_animacion==23
		
	def enemigo_daño(self):
		if heroe_jugador.hechizo_lanzado==True:
			if self.hitbox.colliderect(heroe_jugador.hitbox_hechizo) == True:
				self.vida -= 1
				self.siendo_atacado=True


	def patrullar_lizard(self,xi,xf):
		global daño_recibido
		self.xi=xi
		self.xf=xf
		if self.num_animacion<18:
			if self.vida > 0:
				if self.direccion=="":
					self.direccion="derecha"

				if self.hitbox.x<=self.xi:
					self.direccion="derecha"
				elif self.hitbox.x>=self.xf:
					self.direccion="izquierda"

				if self.direccion=="derecha":
					self.hitbox.x+=random.randint(2,9)
				elif self.direccion=="izquierda":
					self.hitbox.x-=random.randint(2,9)

			if self.hitbox.colliderect(heroe_jugador.hitbox)==True:
				daño_recibido=True

			self.animar_lizard()

	def patrullar_calavera(self,xi,xf,yi,yf):
		global daño_recibido
		self.xi=xi
		self.xf=xf
		self.yi=yi
		self.yf=yf


		if self.direcciony=="":
			self.direcciony="arriba"
		if self.direccion=="":
			self.direccion="derecha"

		if self.hitbox.x<=self.xi:
			self.direccion="derecha"
		elif self.hitbox.x>=self.xf:
			self.direccion="izquierda"


		if self.hitbox.y<=self.yi:
			self.direcciony="abajo"
		elif self.hitbox.y>=self.yf:
			self.direcciony="arriba"

		if self.direccion=="derecha":
			self.hitbox.x+=random.randint(2,7)
		elif self.direccion=="izquierda":
			self.hitbox.x-=random.randint(2,7)
		if self.direcciony=="arriba":
			self.hitbox.y-=random.randint(2,7)
		elif self.direcciony=="abajo":
			self.hitbox.y+=random.randint(2,7)

		if self.hitbox.colliderect(heroe_jugador.hitbox)==True:
			daño_recibido=True

			self.animar_calavera()
	def posiciones(self):
		global nivel
		if nivel==1:
			lizard[0].hitbox.x=random.randint(285,385)
			lizard[0].hitbox.y=355
			lizard[1].hitbox.x=random.randint(105,290)
			lizard[1].hitbox.y=235

			calaveras[0].hitbox.x=random.randint(385,820)
			calaveras[0].hitbox.y=245
			calaveras[1].hitbox.x=random.randint(290,815)
			calaveras[1].hitbox.y=235
			for x in lizard:
				x.vida=1

		if nivel==2:
			lizard[0].hitbox.x=random.randint(285,385)
			lizard[0].hitbox.y=45
			lizard[1].hitbox.x=random.randint(800,900)
			lizard[1].hitbox.y=85

			dragon[0].hitbox.x=270
			dragon[0].hitbox.y=190
			dragon[0].direccion="derecha"
			dragon[1].hitbox.x=570
			dragon[1].hitbox.y=360
			dragon[1].direccion="izquierda"
			calaveras[0].hitbox.x=random.randint(385,820)
			calaveras[0].hitbox.y=245
			calaveras[1].hitbox.x=random.randint(290,815)
			calaveras[1].hitbox.y=235
			for x in lizard:
				x.vida=1
			for x in dragon:
				x.vida=20
		if nivel==3:
			pass

def movimiento():
	global tiempo_colision_escaleras,salto,tiempo_salto
	tecla= pygame.key.get_pressed()
	colisiona_piso=False	
	colisiona_techo=False
	colisiona_escaleras=False
	colisiona_piso_escalera=False
	for muro in escaleras: 
		if heroe_jugador.hitbox.colliderect(muro.rect)==True:
			hitbox_piso.x=heroe_jugador.posx+7
			hitbox_piso.width=14
			colisiona_escaleras=True
		else:
			hitbox_piso.width=18
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso_escalera=True

	for muro in muros_negros: 
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso=True
	for muro in muros_marrones:
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso=True
	for muro in muros_verdes:
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso=True
	for muro in piedras:
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso=True
	for muro in escaleras:
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso=False
		if hitbox_piso.colliderect(muro.rect)==True:
			colisiona_piso_escalera=True

	if colisiona_piso==False and colisiona_escaleras==False and tiempo_colision_escaleras<=0:
		heroe_jugador.posy+=5

	if colisiona_piso==False and colisiona_piso_escalera==True and tiempo_colision_escaleras<=0:
		heroe_jugador.posy-=5

	#techo

	for muro in muros_verdes:
		if hitbox_techo.colliderect(muro.rect)==True:
			colisiona_techo=True
			tiempo_salto=0
			salto=False
	for muro in muros_marrones:
		if hitbox_techo.colliderect(muro.rect)==True:
			colisiona_techo=True
			tiempo_salto=0
			salto=False
	for muro in muros_negros:
		if hitbox_techo.colliderect(muro.rect)==True:
			colisiona_techo=True
			tiempo_salto=0
			salto=False
	for muro in piedras:
		if hitbox_techo.colliderect(muro.rect)==True:
			colisiona_techo=True
			tiempo_salto=0
			salto=False
	for muro in escaleras:
		if hitbox_techo.colliderect(muro.rect)==True:
			colisiona_techo=False



	heroe_jugador.hechizo(1)
	for x in lizard:
		x.enemigo_daño()
	for x in dragon:
		x.enemigo_daño()

	if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]:
		direccion="derecha"
		hitbox_piso.x=heroe_jugador.posx+5
		if heroe_jugador.posx<995:
			heroe_jugador.posx+=5
			if heroe_jugador.hechizo_lanzado==True:
				heroe_jugador.posx-=3
			ultima_tecla="derecha"
			for muro in muros_verdes:
				if hitbox_derecha.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.right=muro.rect.left
					heroe_jugador.posx=heroe_jugador.hitbox.x
			for muro in muros_marrones:
				if hitbox_derecha.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.right=muro.rect.left
					heroe_jugador.posx=heroe_jugador.hitbox.x
			for muro in muros_negros:
				if hitbox_derecha.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.right=muro.rect.left
					heroe_jugador.posx=heroe_jugador.hitbox.x

			for muro in piedras:
				if hitbox_derecha.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.right=muro.rect.left
					heroe_jugador.posx=heroe_jugador.hitbox.x


	if tecla[pygame.K_LEFT] or tecla[pygame.K_a]:
		heroe_jugador.direccion="izquierda"
		hitbox_piso.x=heroe_jugador.posx+1
		if heroe_jugador.posx>5:
			heroe_jugador.posx-=5
			if heroe_jugador.hechizo_lanzado==True:
				heroe_jugador.posx+=3
			ultima_tecla="izquierda"
			for muro in muros_marrones:
				if hitbox_izquierda.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.left=muro.rect.right
					heroe_jugador.posx=heroe_jugador.hitbox.x
			for muro in muros_negros:
				if hitbox_izquierda.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.left=muro.rect.right
					heroe_jugador.posx=heroe_jugador.hitbox.x
			for muro in muros_verdes:
				if hitbox_izquierda.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.left=muro.rect.right
					heroe_jugador.posx=heroe_jugador.hitbox.x

			for muro in piedras:
				if hitbox_izquierda.colliderect(muro.rect)==True:
					heroe_jugador.hitbox.left=muro.rect.right
					heroe_jugador.posx=heroe_jugador.hitbox.x

	if colisiona_escaleras==True or colisiona_piso_escalera==True:
		if tecla[pygame.K_UP] or tecla[pygame.K_w]:
			heroe_jugador.posy-=5
		if tecla[pygame.K_DOWN]  or tecla[pygame.K_s] :
			if colisiona_piso==False:
				heroe_jugador.posy+=5
		tiempo_colision_escaleras=2
	elif tiempo_colision_escaleras>0:
		tiempo_colision_escaleras-=1

#salto

	if colisiona_techo==False and colisiona_escaleras==False or colisiona_techo==False and colisiona_piso_escalera==True :
		if tecla[pygame.K_UP] or tecla[pygame.K_w]:
			if colisiona_piso==True or colisiona_piso_escalera==True:
				salto=True

		if salto==True:
			tiempo_salto+=1
			if tiempo_salto<=6:
				heroe_jugador.posy-=14
			elif hitbox_piso.colliderect(muro.rect)==False:
				tiempo_salto=0
				salto=False
	colisiona_piso=False	
	colisiona_techo=False
	colisiona_escaleras=False
	colisiona_piso_escalera=False


heroe_jugador=propiedades(780,365,22,22,3) 
lizard=[propiedades(24,355,22,22,1),propiedades(105,235,22,22,1)]
calaveras=[propiedades(random.randint(385,820),245,22,22,1),propiedades(random.randint(290,815),235,22,22,1)]
dragon=[propiedades(270,190,80,40,20),propiedades(570,360,80,40,20)]


heroe_jugador.imagenes([pygame.image.load("imagenes/jugador/idled.png"),
	pygame.image.load("imagenes/jugador/run1d.png"),pygame.image.load("imagenes/jugador/run2d.png"),pygame.image.load("imagenes/jugador/run3d.png"),pygame.image.load("imagenes/jugador/run4d.png"),pygame.image.load("imagenes/jugador/run5d.png"),pygame.image.load("imagenes/jugador/run5d.png"),pygame.image.load("imagenes/jugador/idlei.png"),
	pygame.image.load("imagenes/jugador/run1i.png"),pygame.image.load("imagenes/jugador/run2i.png"),pygame.image.load("imagenes/jugador/run3i.png"),pygame.image.load("imagenes/jugador/run4i.png"),pygame.image.load("imagenes/jugador/run5i.png"),pygame.image.load("imagenes/jugador/run5i.png"),
	pygame.image.load("imagenes/jugador/die1.png"),pygame.image.load("imagenes/jugador/die2.png"),pygame.image.load("imagenes/jugador/die3.png"),pygame.image.load("imagenes/jugador/die4.png"),pygame.image.load("imagenes/jugador/die5.png"),pygame.image.load("imagenes/jugador/die5.png")])


lizard_imagenes=[pygame.image.load("imagenes/lizard/Walk1d.png"),
	pygame.image.load("imagenes/lizard/Walk2d.png"),pygame.image.load("imagenes/lizard/Walk3d.png"),pygame.image.load("imagenes/lizard/Walk4d.png"),pygame.image.load("imagenes/lizard/Walk5d.png"),pygame.image.load("imagenes/lizard/Walk6d.png"),
	pygame.image.load("imagenes/lizard/Walk1i.png"),pygame.image.load("imagenes/lizard/Walk2i.png"),pygame.image.load("imagenes/lizard/Walk3i.png"),pygame.image.load("imagenes/lizard/Walk4i.png"),pygame.image.load("imagenes/lizard/Walk5i.png"),pygame.image.load("imagenes/lizard/Walk6i.png"),
	pygame.image.load("imagenes/lizard/Death1.png"),pygame.image.load("imagenes/lizard/Death2.png"),pygame.image.load("imagenes/lizard/Death3.png"),pygame.image.load("imagenes/lizard/Death4.png"),pygame.image.load("imagenes/lizard/Death5.png"),pygame.image.load("imagenes/lizard/Death6.png"),pygame.image.load("imagenes/lizard/Death6.png")]

calavera_imagenes=[
pygame.image.load("imagenes/calaveras/calavera1d.png"),pygame.image.load("imagenes/calaveras/calavera2d.png"),pygame.image.load("imagenes/calaveras/calavera3d.png"),pygame.image.load("imagenes/calaveras/calavera4d.png"),
pygame.image.load("imagenes/calaveras/calavera5d.png"),pygame.image.load("imagenes/calaveras/calavera6d.png"),pygame.image.load("imagenes/calaveras/calavera7d.png"),pygame.image.load("imagenes/calaveras/calavera8d.png"),pygame.image.load("imagenes/calaveras/calavera8d.png"),

pygame.image.load("imagenes/calaveras/calavera1i.png"),pygame.image.load("imagenes/calaveras/calavera2i.png"),pygame.image.load("imagenes/calaveras/calavera3i.png"),pygame.image.load("imagenes/calaveras/calavera4i.png"),
pygame.image.load("imagenes/calaveras/calavera5i.png"),pygame.image.load("imagenes/calaveras/calavera6i.png"),pygame.image.load("imagenes/calaveras/calavera7i.png"),pygame.image.load("imagenes/calaveras/calavera8i.png"),pygame.image.load("imagenes/calaveras/calavera8i.png")
]

dragon_imagenes=[
	pygame.image.load("imagenes/dragon/Idle1d.png"),pygame.image.load("imagenes/dragon/Idle2d.png"),pygame.image.load("imagenes/dragon/Idle3d.png"),
	pygame.image.load("imagenes/dragon/Attack1d.png"),pygame.image.load("imagenes/dragon/Attack2d.png"),pygame.image.load("imagenes/dragon/Attack3d.png"),
	pygame.image.load("imagenes/dragon/Hurt1d.png"),pygame.image.load("imagenes/dragon/Hurt2d.png"),
	pygame.image.load("imagenes/dragon/Death1d.png"),pygame.image.load("imagenes/dragon/Death2d.png"),pygame.image.load("imagenes/dragon/Death3d.png"),pygame.image.load("imagenes/dragon/Death4d.png"),pygame.image.load("imagenes/dragon/Death4d.png"),
	pygame.image.load("imagenes/dragon/Fire_Attack1d.png"),pygame.image.load("imagenes/dragon/Fire_Attack2d.png"),pygame.image.load("imagenes/dragon/Fire_Attack3d.png"),

#15
	pygame.image.load("imagenes/dragon/Idle1i.png"),pygame.image.load("imagenes/dragon/Idle2i.png"),pygame.image.load("imagenes/dragon/Idle3i.png"),
	pygame.image.load("imagenes/dragon/Attack1i.png"),pygame.image.load("imagenes/dragon/Attack2i.png"),pygame.image.load("imagenes/dragon/Attack3i.png"),
	pygame.image.load("imagenes/dragon/Hurt1i.png"),pygame.image.load("imagenes/dragon/Hurt2i.png"),
	pygame.image.load("imagenes/dragon/Death1i.png"),pygame.image.load("imagenes/dragon/Death2i.png"),pygame.image.load("imagenes/dragon/Death3i.png"),pygame.image.load("imagenes/dragon/Death4i.png"),pygame.image.load("imagenes/dragon/Death4i.png"),
	pygame.image.load("imagenes/dragon/Fire_Attack1i.png"),pygame.image.load("imagenes/dragon/Fire_Attack2i.png"),pygame.image.load("imagenes/dragon/Fire_Attack3i.png"),
]


tiempo_colision_escaleras=0

corazon= pygame.image.load("imagenes/objetos/hearth_small.png")

def vidas():
	if lista_vidas[0]==1:
		screen.blit(corazon,(10,10))
	if lista_vidas[1]==1:
		screen.blit(corazon,(50,10))
	if lista_vidas[2]==1:
		screen.blit(corazon,(90,10))

lista_vidas=[1,1,1]

def blit_texto(surface, texto, pos_inicial,pos_final, font, color=((255,0,0))):
    palabras = [palabra.split(' ') for palabra in texto.splitlines()] 
    espacio = font.size(' ')[0]  
    max_width, max_height = pos_final[0],pos_final[1]
    x, y = pos_inicial
    for line in palabras:
        for palabra in line:
            palabra_surface = font.render(palabra, 0, color)
            palabra_width, palabra_height = palabra_surface.get_size()
            if x + palabra_width >= max_width:
                x = pos_inicial[0]  
                y += palabra_height  
            surface.blit(palabra_surface, (x, y))
            x += palabra_width + espacio
        x = pos_inicial[0]  
        y += palabra_height  

#botones y lbl
lbl_jugar = fuente.render('Iniciar', True, (255,0,0)) 
lbl_jugarRect = lbl_jugar.get_rect() 
lbl_jugarRect.center = (500, 80) 

lbl_salir = fuente.render('Salir', True, (255,0,0)) 
lbl_salirRect = lbl_salir.get_rect() 
lbl_salirRect.center = (500, 320) 

lbl_creditos = fuente.render('Creditos', True, (255,0,0)) 
lbl_creditosRect = lbl_creditos.get_rect() 
lbl_creditosRect.center = (500, 200) 


lbl_Creadores = fuente.render('Creadores:', True, (255,0,0)) 
lbl_CreadoresRect = lbl_Creadores.get_rect() 
lbl_CreadoresRect.center = (170, 160)

lbl_Volver = fuente.render('Volver', True, (255,0,0)) 
lbl_VolverRect = lbl_Volver.get_rect() 
lbl_VolverRect.center = (230, 320)

lbl_salir = fuente.render('Salir', True, (255,0,0)) 
lbl_salirRect = lbl_salir.get_rect() 
lbl_salirRect.center = (500, 320)


lbl_jugar_nuevamente = fuente.render('Jugar Nuevamente', True, (255,0,0)) 
lbl_jugar_nuevamenteRect = lbl_jugar_nuevamente.get_rect() 
lbl_jugar_nuevamenteRect.center = (500, 320) 

jugar = Botones((0,255,0),350,50,325,60)
salir = Botones((0,255,0),350,50,325,300)
creditos = Botones((0,255,0),350,50,325,180)
Volver = Botones((0,255,0),350,50,70,300)
jugar_nuevamente = Botones((0,255,0),350,50,325,300)

reinicio_nivel=0
reinicio_juego=0

animacion_actual=""
menu=True
juego=True
iniciar=0
salto=False
tiempo_salto=0

llave_estado=False

hitbox_derecha=pygame.Rect(5, 5, 2, 19)
hitbox_izquierda=pygame.Rect(5, 5, 2, 19)
hitbox_piso=pygame.Rect(5, 5, 18, 3)
hitbox_techo=pygame.Rect(5, 5, 15, 2)

#hitbox_vigilante = pygame.Rect(22, 20)
nivel=0
ultima_tecla=""

refresh=0
t0=0
llave=propiedades(60, 335, 21, 15,0)
puerta=propiedades(840,15, 65, 65,0)

daño_recibido=False

while True:
	while menu==True:
		for event in pygame.event.get():
			if event.type== QUIT:
				menu=False
				juego=False
				pygame.quit()
				os._exit(1)
				quit()

			if iniciar==0:
				if refresh==0:
					screen = pygame.display.set_mode((940, 380))
					refresh=1
				screen.fill((0,0,0))
				pygame.draw.rect(screen, salir.color, (salir.posx, salir.posy, salir.width, salir.height))
				pygame.draw.rect(screen, jugar.color, (jugar.posx, jugar.posy, jugar.width, jugar.height))
				pygame.draw.rect(screen, creditos.color, (creditos.posx, creditos.posy, creditos.width, creditos.height))
				screen.blit(lbl_jugar, lbl_jugarRect)
				screen.blit(lbl_salir, lbl_salirRect)
				screen.blit(lbl_creditos, lbl_creditosRect)

				pos = pygame.mouse.get_pos()
				if event.type==pygame.MOUSEBUTTONDOWN:
					if jugar.click(pos):
						screen.fill((0,0,0))
						menu=False
						jugar=True
					if salir.click(pos):
						pygame.quit()
					if creditos.click(pos):
						screen.fill((0,0,0))
						iniciar=1

				tecla=pygame.key.get_pressed()
				if tecla[pygame.K_ESCAPE]:
					pygame.quit()

			elif iniciar==1:
				screen.fill((0,0,0))
				pygame.draw.rect(screen, Volver.color, (Volver.posx, Volver.posy, Volver.width, Volver.height))
				screen.blit(lbl_Creadores, lbl_CreadoresRect)
				screen.blit(lbl_Volver, lbl_VolverRect)
				blit_texto(screen, "Lucas Silva, Lucas Nocquet y Lautaro Molina", (275, 125),(640,300), fuente)
				
				pos = pygame.mouse.get_pos()
				if event.type==pygame.MOUSEBUTTONDOWN:
					if Volver.click(pos):
						screen.fill((0,0,0))
						iniciar=0
                                         

		pygame.display.update()

	while juego==True:
		for event in pygame.event.get():
			if event.type== QUIT:
				menu=False
				juego=False
				pygame.quit()
				os._exit(1)
				quit()
			if tecla[pygame.K_ESCAPE]:
				pygame.quit()

		if refresh==1:
			screen = pygame.display.set_mode((940, 480))
			refresh=0
			cargar_nivel(nivel)



		screen.fill((0,0,0))
		if modo=="admin":
			pos = pygame.mouse.get_pos()
			if event.type==pygame.MOUSEBUTTONDOWN:
				heroe_jugador.posx=pos[0]
				heroe_jugador.posy=pos[1]


		#escenario
		#pygame.draw.rect(screen, (240,0,0), (lizard.hitbox.x,lizard.hitbox.y,lizard.hitbox.width,lizard.hitbox.height))

		
		#pygame.draw.rect(screen, (240,0,0), (heroe_jugador.hitbox.x,heroe_jugador.hitbox.y,heroe_jugador.hitbox.width,heroe_jugador.hitbox.height))
		#pygame.draw.rect(screen, (240,0,0), (hitbox_derecha.x,hitbox_derecha.y,hitbox_derecha.width,hitbox_derecha.height))
		#pygame.draw.rect(screen, (240,0,0), (hitbox_izquierda.x,hitbox_izquierda.y,hitbox_izquierda.width,hitbox_izquierda.height))
		#pygame.draw.rect(screen, (240,0,0), (hitbox_piso.x,hitbox_piso.y,hitbox_piso.width,hitbox_piso.height))
		#pygame.draw.rect(screen, (240,0,0), (hitbox_techo.x,hitbox_techo.y,hitbox_techo.width,hitbox_techo.height))

		if reinicio_nivel==1:
			llave_estado=False
			#añadir futuras actualizaciones para el reinicio
			for x in lizard:
				x.posiciones()
			for x in calaveras:
				x.posiciones()
			for x in dragon:
				x.posiciones()
				x.dragon_hechizo.clear()

			daño_recibido=False 
			if nivel==0:
				heroe_jugador.posx=780
				heroe_jugador.posy=365
			if nivel==1:
				heroe_jugador.posx=60
				heroe_jugador.posy=365
			elif nivel==2:
				heroe_jugador.posx=25
				heroe_jugador.posy=25
			elif nivel==3:
				heroe_jugador.posx=25
				heroe_jugador.posy=25
		reinicio_nivel=0



		for muro in muros_verdes:
			pygame.draw.rect(screen, (0, 143, 57), muro.rect)
		for muro in muros_marrones:
			pygame.draw.rect(screen, (128, 64, 0), muro.rect)
		for muro in muros_negros:
			pygame.draw.rect(screen, (45, 45, 45), muro.rect)
		for muro in lavas:
			pygame.draw.rect(screen, (255, 128, 0), muro.rect)
		for muro in escaleras:
			pygame.draw.rect(screen, (0, 0, 0), muro.rect)
			screen.blit(pygame.image.load("imagenes/objetos/escalera.png"),(muro.x,muro.y))
		for muro in piedras:
			pygame.draw.rect(screen, (80, 57, 38), muro.rect)
		if nivel==0:

			llave.hitbox=pygame.Rect(60, 255, 21, 15)
			puerta.hitbox=pygame.Rect(50,305, 65, 65)
			lizard[0].hitbox.y=265
			lizard[0].patrullar_lizard(25,130)
			lizard[0].animar_lizard()
			t0+=1
			if t0<=100:
				blit_texto(screen, "Consigue la llave para que la puerta se abra", (275, 205),(640,300), fuente)
			elif t0<190:
				blit_texto(screen, "Utiliza la tecla espacio para lanzar hechizos", (275, 205),(640,300), fuente)
			elif t0<250:
				blit_texto(screen, "ten cuidado, los hechizos te relentizaran!", (275, 205),(640,300), fuente)

			else:
				blit_texto(screen, "", (275, 205),(640,300), fuente)

			if llave_estado==False:
				
				screen.blit(pygame.image.load("imagenes/objetos/llave.png"),(llave.hitbox.x,llave.hitbox.y))
				screen.blit(pygame.image.load("imagenes/objetos/puerta1.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if hitbox_derecha.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx-=5
				elif hitbox_izquierda.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx+=5
			else:
				screen.blit(pygame.image.load("imagenes/objetos/puerta2.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if heroe_jugador.hitbox.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx=60
					heroe_jugador.posy=365
					nivel=1
					for x in lizard:
						x.posiciones()
						x.vida=1
					for x in calaveras:
						x.posiciones()
					llave_estado=False
					cargar_nivel(nivel)
			if heroe_jugador.hitbox.colliderect(llave.hitbox)==True:
				llave_estado=True

		if nivel==1:
			lizard[0].patrullar_lizard(285,385)
			lizard[1].patrullar_lizard(105,290)
			calaveras[0].patrullar_calavera(350,820,150,300)
			calaveras[1].patrullar_calavera(350,870,280,370)

			for x in lizard:
				x.animar_lizard()
			for x in calaveras:
				x.animar_calavera()

			llave.hitbox=pygame.Rect(60, 335, 21, 15)
			puerta.hitbox=pygame.Rect(840,15, 65, 65)

			if llave_estado==False:
				
				screen.blit(pygame.image.load("imagenes/objetos/llave.png"),(llave.hitbox.x,llave.hitbox.y))
				screen.blit(pygame.image.load("imagenes/objetos/puerta1.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if hitbox_derecha.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx-=5
				elif hitbox_izquierda.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx+=5
			else:
				screen.blit(pygame.image.load("imagenes/objetos/puerta2.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if heroe_jugador.hitbox.colliderect(puerta.hitbox)==True:

					heroe_jugador.posx=25
					heroe_jugador.posy=25
					nivel=2
					for x in lizard:
						x.posiciones()
						x.vida=1
					for x in calaveras:
						x.posiciones()
					llave_estado=False
					cargar_nivel(nivel)
			if heroe_jugador.hitbox.colliderect(llave.hitbox)==True:
				llave_estado=True

		elif nivel==2:

			lizard[0].patrullar_lizard(345,495)
			lizard[1].patrullar_lizard(795,900)
			#calaveras[0].patrullar_calavera(350,820,150,300)
			#calaveras[1].patrullar_calavera(350,870,280,370)

			for x in lizard:
				x.animar_lizard()
			for x in dragon:
				x.animar_dragon()
				x.hechizo(2)
			#for x in calaveras:
				#x.animar_calavera()

			llave.hitbox=pygame.Rect(810, 95, 21, 15)
			puerta.hitbox=pygame.Rect(760,365, 65, 65)
			#pygame.draw.rect(screen, (240,0,0), (dragon[0].hitbox.x,dragon[0].hitbox.y,dragon[0].hitbox.width,dragon[0].hitbox.height))

			if llave_estado==False:
				screen.blit(pygame.image.load("imagenes/objetos/llave.png"),(llave.hitbox.x,llave.hitbox.y))
				screen.blit(pygame.image.load("imagenes/objetos/puerta1.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if hitbox_derecha.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx-=5
				elif hitbox_izquierda.colliderect(puerta.hitbox)==True:
					heroe_jugador.posx+=5
			else:
				screen.blit(pygame.image.load("imagenes/objetos/puerta2.png"),(puerta.hitbox.x,puerta.hitbox.y))
				if heroe_jugador.hitbox.colliderect(puerta.hitbox)==True:

					heroe_jugador.posx=25
					heroe_jugador.posy=25
					llave_estado=False
					nivel=3
					cargar_nivel(nivel)
			if heroe_jugador.hitbox.colliderect(llave.hitbox)==True:
				llave_estado=True

		elif nivel==3:
			
			puerta.hitbox=pygame.Rect(840,15, 65, 65)
			#screen.blit(pygame.image.load("imagenes/puerta1.png"),(puerta.hitbox.x,puerta.hitbox.y))



		vidas()

		#pygame.draw.rect(screen, (240,0,0), (llave.hitbox.x,llave.hitbox.y,llave.hitbox.width,llave.hitbox.height))
		#pygame.draw.rect(screen, (240,0,0), (puerta.hitbox.x,puerta.hitbox.y,puerta.hitbox.width,puerta.hitbox.height))
		heroe_jugador.hitbox.x=heroe_jugador.posx
		heroe_jugador.hitbox.y=heroe_jugador.posy
		hitbox_derecha.x=heroe_jugador.posx+25
		hitbox_derecha.y=heroe_jugador.posy
		hitbox_izquierda.x=heroe_jugador.posx-5
		hitbox_izquierda.y=heroe_jugador.posy
		hitbox_piso.x=heroe_jugador.posx+3
		hitbox_piso.y=heroe_jugador.posy+27
		hitbox_techo.x=heroe_jugador.posx+2
		hitbox_techo.y=heroe_jugador.posy-5

		#muerte
		for lava in lavas: 
			if heroe_jugador.hitbox.colliderect(lava.rect)==True:
				daño_recibido=True

		if daño_recibido==True:
			heroe_jugador.hechizo_lanzado=False
			heroe_jugador.tiempo_hechizo=0
			if heroe_jugador.vida>0:
				muerte_sonido = mixer.Sound("sonidos/character_die.wav")
				muerte_sonido.play()
			heroe_jugador.vida-=1
			if lista_vidas==[1,1,1]:
				if heroe_jugador.num_animacion>=18:
					time.sleep(0.1)
					lista_vidas=[1,1,0]
					reinicio_nivel=1
					heroe_jugador.vida=2
			elif lista_vidas==[1,1,0]:
				if heroe_jugador.num_animacion>=18:
					time.sleep(0.1)
					lista_vidas=[1,0,0]
					reinicio_nivel=1
					heroe_jugador.vida=1
			elif lista_vidas==[1,0,0]:
				if heroe_jugador.num_animacion>=18:
					time.sleep(0.1)
					lista_vidas=[0,0,0]
					reinicio_juego=1

		if reinicio_juego==1:
			blit_texto(screen, "Game over", (355, 125),(840,300), pygame.font.SysFont("Arial", 65))
			pygame.draw.rect(screen, jugar_nuevamente.color, (jugar_nuevamente.posx, jugar_nuevamente.posy, jugar_nuevamente.width, jugar_nuevamente.height))
			screen.blit(lbl_jugar_nuevamente, lbl_jugar_nuevamenteRect)
			heroe_jugador.num_animacion=19
			pos = pygame.mouse.get_pos()
			daño_recibido=False
			#reinicio_nivel=1
			if event.type==pygame.MOUSEBUTTONDOWN:
				if jugar_nuevamente.click(pos):
					reinicio_nivel=1
					nivel=1
					heroe_jugador.posx=60
					heroe_jugador.posy=365
					llave_estado=False
					heroe_jugador.vida=3
					lista_vidas=[1,1,1]
					refresh=1
					reinicio_juego=0
		

		if heroe_jugador.vida>0:
			movimiento()

		heroe_jugador.animar()
		
		#pos = pygame.mouse.get_pos()
		#if event.type==pygame.MOUSEBUTTONDOWN:
			#pass

		clock.tick(30)
		pygame.display.update()
