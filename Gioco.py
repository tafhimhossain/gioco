import arcade
import random

class Gioco(arcade.Window):
    def __init__(self, larghezza, altezza, titolo):
        super().__init__(larghezza, altezza, titolo)

        self.sprite = None

        self.lista_sprite = arcade.SpriteList()
        self.lista_caramella = arcade.SpriteList()
        self.lista_velocita = arcade.SpriteList()
        self.lista_tempo = arcade.SpriteList()

        self.suono_mangia = arcade.load_sound("./assets/mangia.mp3")

        self.sfondo = None
        
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.velocita_base = 7
        self.velocita = self.velocita_base
        self.velocita_boost_timer = 0
        
        self.punteggio = 0
        self.timer_iniziale = 30.0
        self.timer = self.timer_iniziale
        self.gioco_finito = False

        # Timer spawn
        self.timer_spawn_tempo = random.choice([3,5,7])
        self.timer_spawn_velocita = random.choice([4,6,8])
        
        self.setup()
    
    def setup(self):
        self.lista_sprite.clear()
        self.lista_caramella.clear()
        self.lista_velocita.clear()
        self.lista_tempo.clear()

        self.punteggio = 0
        self.timer = self.timer_iniziale
        self.gioco_finito = False

        self.velocita = self.velocita_base
        self.velocita_boost_timer = 0

        self.timer_spawn_tempo = random.choice([3,5,7])
        self.timer_spawn_velocita = random.choice([4,6,8])

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
        caramella = arcade.Sprite("./assets/caramella.png")
        caramella.center_x = random.randint(50, self.width - 50)
        caramella.center_y = random.randint(50, self.height - 50)
        caramella.scale = 0.18
        self.lista_caramella.append(caramella)

    def crea_velocita(self):
        velocita = arcade.Sprite("./assets/velocita.png")
        velocita.center_x = random.randint(50, self.width - 50)
        velocita.center_y = random.randint(50, self.height - 50)
        velocita.scale = 0.12
        self.lista_velocita.append(velocita)

    def crea_tempo(self):
        tempo = arcade.Sprite("./assets/tempo.png")
        tempo.center_x = random.randint(50, self.width - 50)
        tempo.center_y = random.randint(50, self.height - 50)
        tempo.scale = 0.35
        self.lista_tempo.append(tempo)
    
    def on_draw(self):
        self.clear()

        self.sfondo.center_x = self.width // 2
        self.sfondo.center_y = self.height // 2
        self.sfondo.width = self.width
        self.sfondo.height = self.height
        arcade.draw_sprite(self.sfondo)

        self.lista_caramella.draw()
        self.lista_velocita.draw()
        self.lista_tempo.draw()
        self.lista_sprite.draw()

        arcade.draw_text(f"Tempo: {max(0, int(self.timer))}", 25, self.height - 50,
                         arcade.color.WHITE, 26, bold=True)

        arcade.draw_text(f"Punti: {self.punteggio}", self.width - 200,
                         self.height - 50, arcade.color.WHITE, 26, bold=True)

        if self.gioco_finito:
            arcade.draw_text(
                f"TEMPO SCADUTO!\nPunti totali: {self.punteggio}", 
                self.width // 2, self.height // 2 + 20,
                arcade.color.WHITE, 40, bold=True,
                anchor_x="center", multiline=True, width=600, align="center"
            )
            
            arcade.draw_text(
                "Premi SPAZIO per ricominciare",
                self.width // 2, self.height // 2 - 80,
                arcade.color.WHITE, 20, bold=True,
                anchor_x="center"
            )
    
    def on_update(self, delta_time):
        if self.gioco_finito:
            return

        # Timer principale
        self.timer -= delta_time
        if self.timer <= 0:
            self.timer = 0
            self.gioco_finito = True

        # Spawn tempo
        self.timer_spawn_tempo -= delta_time
        if self.timer_spawn_tempo <= 0:
            self.crea_tempo()
            self.timer_spawn_tempo = random.choice([3,5,7])

        # Spawn velocita
        self.timer_spawn_velocita -= delta_time
        if self.timer_spawn_velocita <= 0:
            self.crea_velocita()
            self.timer_spawn_velocita = random.choice([4,6,8])

        # Gestione effetto velocità
        if self.velocita_boost_timer > 0:
            self.velocita_boost_timer -= delta_time
            if self.velocita_boost_timer <= 0:
                self.velocita = self.velocita_base

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

        self.sprite.center_x = max(0, min(self.width, self.sprite.center_x))
        self.sprite.center_y = max(0, min(self.height, self.sprite.center_y))
        
        # Collisione caramella
        collisioni = arcade.check_for_collision_with_list(self.sprite, self.lista_caramella)
        if collisioni:
            arcade.play_sound(self.suono_mangia)
            self.punteggio += 1
            for c in collisioni:
                c.remove_from_sprite_lists()
            self.crea_caramella()

        # Collisione velocita
        collisioni_vel = arcade.check_for_collision_with_list(self.sprite, self.lista_velocita)
        if collisioni_vel:
            self.velocita = self.velocita_base + 4
            self.velocita_boost_timer = 2  # dura 2 secondi
            for v in collisioni_vel:
                v.remove_from_sprite_lists()

        # Collisione tempo
        collisioni_temp = arcade.check_for_collision_with_list(self.sprite, self.lista_tempo)
        if collisioni_temp:
            self.timer += 2  # +2 secondi
            for t in collisioni_temp:
                t.remove_from_sprite_lists()
    
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