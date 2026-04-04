import arcade
import random

CLASSIFICA_FILE = "classifica.txt"
MAX_PUNTEGGI = 10


def carica_classifica():
    try:
        with open(CLASSIFICA_FILE, "r") as f:
            righe = f.read().strip().splitlines()
        return [int(r) for r in righe if r.strip().isdigit()]
    except Exception:
        return []


def salva_classifica(classifica):
    try:
        with open(CLASSIFICA_FILE, "w") as f:
            f.write("\n".join(str(p) for p in classifica))
    except Exception:
        pass


def aggiorna_classifica(punteggio):
    try:
        classifica = carica_classifica()
        classifica.append(punteggio)
        classifica.sort(reverse=True)
        classifica = classifica[:MAX_PUNTEGGI]
        salva_classifica(classifica)
        return classifica
    except Exception:
        return [punteggio]


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

        self.velocita_base = 8
        self.velocita = self.velocita_base
        self.velocita_boost_timer = 0

        self.punteggio = 0
        self.timer_iniziale = 30.0
        self.timer = self.timer_iniziale
        self.gioco_finito = False

        self.timer_spawn_tempo = random.choice([3, 5, 7])
        self.timer_spawn_velocita = random.choice([4, 6, 8])

        self.classifica = carica_classifica()
        self.record = self.classifica[0] if self.classifica else 0
        self.classifica_aggiornata = []
        self.nuovo_record = False

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

        self.timer_spawn_tempo = random.choice([3, 5, 7])
        self.timer_spawn_velocita = random.choice([4, 6, 8])

        self.classifica_aggiornata = []
        self.nuovo_record = False

        self.sfondo = arcade.Sprite("./assets/sfondo.png")
        self.sfondo.center_x = self.width // 2
        self.sfondo.center_y = self.height // 2

        self.sprite = arcade.Sprite("./assets/sprite.png")
        self.sprite.center_x = 300
        self.sprite.center_y = 100
        self.sprite.scale = 0.4
        self.lista_sprite.append(self.sprite)

        self.crea_caramella()

    def crea_caramella(self):
        caramella = arcade.Sprite("./assets/caramella.png")
        caramella.center_x = random.randint(50, self.width - 50)
        caramella.center_y = random.randint(50, self.height - 50)
        caramella.scale = 0.12
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
        tempo.scale = 0.40
        self.lista_tempo.append(tempo)

    def disegna_classifica(self):
        panel_w = 420
        panel_h = 420
        panel_x = self.width // 2
        panel_y = self.height // 2

        arcade.draw_rect_filled(
            arcade.XYWH(panel_x, panel_y, panel_w, panel_h),
            (0, 0, 0, 180)
        )
        arcade.draw_rect_outline(
            arcade.XYWH(panel_x, panel_y, panel_w, panel_h),
            arcade.color.GOLD, 3
        )

        arcade.draw_text("TEMPO SCADUTO!", panel_x, panel_y + 170,
                         arcade.color.WHITE, 32, bold=True,
                         anchor_x="center")

        colore_punteggio = arcade.color.GOLD if self.nuovo_record else arcade.color.WHITE
        testo_punteggio = f"Punti: {self.punteggio}"
        if self.nuovo_record:
            testo_punteggio += "  * NUOVO RECORD!"
        arcade.draw_text(testo_punteggio, panel_x, panel_y + 130,
                         colore_punteggio, 22, bold=True, anchor_x="center")

        record = self.classifica_aggiornata[0] if self.classifica_aggiornata else 0
        if not self.nuovo_record and record > 0:
            arcade.draw_text(f"Record da battere: {record}", panel_x,
                             panel_y + 100, arcade.color.LIGHT_YELLOW, 18,
                             anchor_x="center")

        arcade.draw_text("-- CLASSIFICA --", panel_x, panel_y + 65,
                         arcade.color.LIGHT_GRAY, 16, bold=True,
                         anchor_x="center")

        col_x_num = panel_x - 160
        col_x_score = panel_x + 130
        y_start = panel_y + 35

        for i, pts in enumerate(self.classifica_aggiornata[:8]):
            y = y_start - i * 34

            if i == 0:
                colore = arcade.color.GOLD
                dim = 20
            elif i == 1:
                colore = arcade.color.LIGHT_GRAY
                dim = 18
            elif i == 2:
                colore = (205, 127, 50)
                dim = 17
            else:
                colore = arcade.color.WHITE
                dim = 16

            arcade.draw_text(f"{i + 1}.", col_x_num, y,
                             colore, dim, bold=(i < 3), anchor_x="center")
            arcade.draw_text(str(pts), col_x_score, y,
                             colore, dim, bold=(i < 3), anchor_x="right")

            if record > 0:
                barra_max = 200
                barra_w = max(1, int((pts / record) * barra_max))
                barra_x = col_x_num + 20
                arcade.draw_rect_filled(
                    arcade.XYWH(barra_x + barra_w // 2, y + 8, barra_w, 14),
                    (*colore[:3], 80)
                )
                arcade.draw_rect_outline(
                    arcade.XYWH(barra_x + barra_max // 2, y + 8, barra_max, 14),
                    (*colore[:3], 40), 1
                )

        arcade.draw_text("Premi SPAZIO per ricominciare",
                         panel_x, panel_y - 185,
                         arcade.color.WHITE, 18, bold=True, anchor_x="center")

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

        arcade.draw_text(f"Tempo: {max(0, int(self.timer))}", 25,
                         self.height - 50, arcade.color.WHITE, 26, bold=True)
        arcade.draw_text(f"Punti: {self.punteggio}", self.width - 200,
                         self.height - 50, arcade.color.WHITE, 26, bold=True)

        record = self.classifica[0] if self.classifica else 0
        if record > 0:
            colore_rec = (arcade.color.GOLD
                          if self.punteggio >= record
                          else arcade.color.LIGHT_YELLOW)
            arcade.draw_text(f"Record: {record}", self.width // 2,
                             self.height - 50, colore_rec, 20, bold=True,
                             anchor_x="center")

        if self.gioco_finito:
            self.disegna_classifica()

    def on_update(self, delta_time):
        if self.gioco_finito:
            return

        self.timer -= delta_time
        if self.timer <= 0:
            self.timer = 0
            self.gioco_finito = True
            self.classifica_aggiornata = aggiorna_classifica(self.punteggio)
            self.classifica = list(self.classifica_aggiornata)
            self.record = self.classifica[0] if self.classifica else 0
            self.nuovo_record = (
                self.punteggio > 0
                and len(self.classifica_aggiornata) > 0
                and self.classifica_aggiornata[0] == self.punteggio
                and self.classifica_aggiornata.count(self.punteggio) == 1
            )
            return

        self.timer_spawn_tempo -= delta_time
        if self.timer_spawn_tempo <= 0:
            self.crea_tempo()
            self.timer_spawn_tempo = random.choice([3, 5, 7])

        self.timer_spawn_velocita -= delta_time
        if self.timer_spawn_velocita <= 0:
            self.crea_velocita()
            self.timer_spawn_velocita = random.choice([4, 6, 8])

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
            self.sprite.scale = (0.4, 0.4)
        elif change_x > 0:
            self.sprite.scale = (-0.4, 0.4)

        self.sprite.center_x = max(0, min(self.width, self.sprite.center_x))
        self.sprite.center_y = max(0, min(self.height, self.sprite.center_y))

        collisioni = arcade.check_for_collision_with_list(
            self.sprite, self.lista_caramella)
        if collisioni:
            arcade.play_sound(self.suono_mangia)
            self.punteggio += 1
            for c in collisioni:
                c.remove_from_sprite_lists()
            self.crea_caramella()

        collisioni_vel = arcade.check_for_collision_with_list(
            self.sprite, self.lista_velocita)
        if collisioni_vel:
            self.velocita = self.velocita_base + 4
            self.velocita_boost_timer = 2
            for v in collisioni_vel:
                v.remove_from_sprite_lists()

        collisioni_temp = arcade.check_for_collision_with_list(
            self.sprite, self.lista_tempo)
        if collisioni_temp:
            self.timer += 2
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