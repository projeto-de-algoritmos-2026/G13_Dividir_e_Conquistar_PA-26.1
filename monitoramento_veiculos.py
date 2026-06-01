import tkinter as tk
from random import randint
from math import sqrt

# ==========================
# CONTADORES
# ==========================

comparacoes_dividir_conquistar = 0

# ==========================
# ALGORITMO
# ==========================

def distancia(p1, p2):
    global comparacoes_dividir_conquistar

    comparacoes_dividir_conquistar += 1

    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def total_comparacoes_forca_bruta(n):
    return n * (n - 1) // 2


def brute_force(points):
    n = len(points)

    if n < 2:
        return float('inf'), None, None

    min_dist = float('inf')
    p1 = None
    p2 = None

    for i in range(n):
        for j in range(i + 1, n):

            d = distancia(points[i], points[j])

            if d < min_dist:
                min_dist = d
                p1 = points[i]
                p2 = points[j]

    return min_dist, p1, p2


def closest_pair_recursive(px):

    n = len(px)

    if n <= 3:
        return brute_force(px)

    mid = n // 2
    midpoint = px[mid]

    left = px[:mid]
    right = px[mid:]

    dl, pl1, pl2 = closest_pair_recursive(left)
    dr, pr1, pr2 = closest_pair_recursive(right)

    if dl < dr:
        d = dl
        best_p1 = pl1
        best_p2 = pl2
    else:
        d = dr
        best_p1 = pr1
        best_p2 = pr2

    strip = []

    for point in px:
        if abs(point[0] - midpoint[0]) < d:
            strip.append(point)

    strip.sort(key=lambda p: p[1])

    m = len(strip)

    for i in range(m):
        j = i + 1

        while j < m and (strip[j][1] - strip[i][1]) < d:

            dist = distancia(strip[i], strip[j])

            if dist < d:
                d = dist
                best_p1 = strip[i]
                best_p2 = strip[j]

            j += 1

    return d, best_p1, best_p2


def closest_pair(points):

    global comparacoes_dividir_conquistar

    comparacoes_dividir_conquistar = 0

    if len(points) < 2:
        return None

    px = sorted(points, key=lambda p: p[0])

    return closest_pair_recursive(px)


# ==========================
# INTERFACE
# ==========================

class App:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema de Monitoramento de Veículos")

        self.points = []

        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)

        self.btn_random = tk.Button(
            self.frame_top,
            text="Gerar 20 Veículos",
            command=self.gerar_aleatorios
        )
        self.btn_random.grid(row=0, column=0, padx=5)

        self.btn_find = tk.Button(
            self.frame_top,
            text="Encontrar Mais Próximos",
            command=self.encontrar
        )
        self.btn_find.grid(row=0, column=1, padx=5)

        self.btn_clear = tk.Button(
            self.frame_top,
            text="Limpar",
            command=self.limpar
        )
        self.btn_clear.grid(row=0, column=2, padx=5)

        self.canvas = tk.Canvas(
            root,
            width=800,
            height=500,
            bg="white"
        )

        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.adicionar_ponto)

        self.label = tk.Label(
            root,
            text="Clique no mapa para adicionar veículos."
        )

        self.label.pack(pady=10)

    # ==========================

    def desenhar_ponto(self, x, y, cor="blue"):

        r = 5

        self.canvas.create_oval(
            x-r,
            y-r,
            x+r,
            y+r,
            fill=cor,
            outline=cor
        )

    # ==========================

    def adicionar_ponto(self, event):

        ponto = (event.x, event.y)

        self.points.append(ponto)

        self.desenhar_ponto(event.x, event.y)

    # ==========================

    def gerar_aleatorios(self):

        self.limpar()

        for _ in range(20):

            x = randint(20, 780)
            y = randint(20, 480)

            self.points.append((x, y))

            self.desenhar_ponto(x, y)

    # ==========================

    def limpar(self):

        self.canvas.delete("all")
        self.points.clear()

        self.label.config(
            text="Mapa limpo."
        )

    # ==========================

    def encontrar(self):

        if len(self.points) < 2:

            self.label.config(
                text="Adicione pelo menos 2 veículos."
            )

            return

        resultado = closest_pair(self.points)

        if resultado is None:
            return

        dist, p1, p2 = resultado

        self.canvas.delete("highlight")

        r = 8

        self.canvas.create_oval(
            p1[0]-r,
            p1[1]-r,
            p1[0]+r,
            p1[1]+r,
            outline="red",
            width=3,
            tags="highlight"
        )

        self.canvas.create_oval(
            p2[0]-r,
            p2[1]-r,
            p2[0]+r,
            p2[1]+r,
            outline="red",
            width=3,
            tags="highlight"
        )

        self.canvas.create_line(
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            fill="red",
            width=2,
            tags="highlight"
        )

        total_fb = total_comparacoes_forca_bruta(len(self.points))

        self.label.config(
            text=(
                f"Menor distância: {dist:.2f} | "
                f"Dividir e Conquistar: {comparacoes_dividir_conquistar} comparações | "
                f"Força Bruta: {total_fb} comparações"
            )
        )


# ==========================
# EXECUÇÃO
# ==========================

root = tk.Tk()

app = App(root)

root.mainloop()