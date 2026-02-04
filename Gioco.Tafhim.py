import arcade
import random

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.sprite = None
        self.caramella = None
        self.lista_sprite = arcade.SpriteList()
        self.lista_caramella = arcade.SpriteList()
        self.suono_mangia = arcade.load_sound("./assets/mangia.mp3")

        self.sfondo = None
        
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.velocita = 7
        
    
        self.punteggio = 0
        self.timer_iniziale = 30.0
        self.timer = self.timer_iniziale
        self.gioco_finito = False
        
        self.setup()
    
    def setup(self):
        self.lista_sprite.clear()
        self.lista_caramella.clear()
        self.punteggio = 0
        self.timer = self.timer_iniziale
        self.gioco_finito = False

        self.sfondo = arcade.Sprite("./assets/sfondo.png")
        self.sfondo.center_x = self.width // 2
        self.sfondo.center_y = self.height // 2

        self.sprite = arcade.Sprite("./assets/sprite.png")
        self.sprite.center_x = 300
        self.sprite.center_y = 100
        self.sprite.scale = 0.5
        self.lista_sprite.append(self.sprite)
        
        self.crea_caramella()
    
    def crea_caramella(self):
        self.caramella = arcade.Sprite("./assets/caramella.png")
        self.caramella.center_x = random.randint(50, self.width - 50)
        self.caramella.center_y = random.randint(50, self.height - 50)
        self.caramella.scale = 0.15
        self.lista_caramella.append(self.caramella)
    
    def on_draw(self):
        self.clear()

        self.sfondo.center_x = self.width // 2
        self.sfondo.center_y = self.height // 2
        self.sfondo.width = self.width
        self.sfondo.height = self.height
        arcade.draw_sprite(self.sfondo)

        self.lista_caramella.draw()
        self.lista_sprite.draw()

        testo_timer = f"Tempo: {max(0, int(self.timer))}"
        arcade.draw_text(testo_timer, 25, self.height - 50, arcade.color.WHITE, 26, bold=True)

        testo_punti = f"Punti: {self.punteggio}"
        arcade.draw_text(testo_punti, self.width - 200, self.height - 50, arcade.color.WHITE, 26, bold=True)

        if self.gioco_finito:
            arcade.draw_text(f"TEMPO SCADUTO!\nPunti totali: {self.punteggio}", 
                             self.width // 2, self.height // 2 + 20, 
                             arcade.color.WHITE, 40, bold=True, 
                             anchor_x="center", multiline=True, width=600, align="center")
            
            arcade.draw_text("Premi SPAZIO per ricominciare", 
                             self.width // 2, self.height // 2 - 80, 
                             arcade.color.WHITE, 20, bold=True, anchor_x="center")
    
    def on_update(self, delta_time):
        if self.gioco_finito:
            return

        self.timer -= delta_time
        if self.timer <= 0:
            self.timer = 0
            self.gioco_finito = True

        change_x = 0
        change_y = 0
        
        if self.up_pressed:
            change_y += self.velocita
        if self.down_pressed:
            change_y -= self.velocita
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita
        
        self.sprite.center_x += change_x
        self.sprite.center_y += change_y
        
        if change_x < 0: 
            self.sprite.scale = (0.5, 0.5)
        elif change_x > 0:
            self.sprite.scale = (-0.5, 0.5)
        
        if self.sprite.center_x < 0:
            self.sprite.center_x = 0
        elif self.sprite.center_x > self.width:
            self.sprite.center_x = self.width
        
        if self.sprite.center_y < 0:
            self.sprite.center_y = 0
        elif self.sprite.center_y > self.height:
            self.sprite.center_y = self.height
        
        collisioni = arcade.check_for_collision_with_list(self.sprite, self.lista_caramella)
        
        if len(collisioni) > 0:
            arcade.play_sound(self.suono_mangia)
            self.punteggio += 1
            for caramella in collisioni:
                caramella.remove_from_sprite_lists()
            self.crea_caramella()
    
    def on_key_press(self, tasto, modificatori):
        if self.gioco_finito and tasto == arcade.key.SPACE:
            self.setup()

        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
    
    def on_key_release(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False

def main():
    gioco = Gioco(1000, 600, "Gioco")
    arcade.run()

if __name__ == "__main__":
    main()