from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import export_png

def crear_grafico(x, y, name, id1, brightness, id2, title_graph, lines, title_pic):
    # Crear la fuente de datos
    source = ColumnDataSource(data=dict(
        x=x, y=y, name=name, id1=id1, brightness=brightness, id2=id2))

    fig = figure(title=title_graph, x_axis_label='X', y_axis_label='Y',
                 tools="pan,wheel_zoom,box_zoom,reset,save")

    # Agregar los puntos al gráfico
    circles = fig.circle('x', 'y', source=source, size=10)

    # Dibujar linea
    if lines:
        fig.line('x', 'y', source=source, line_width=2)

    # Agregar la herramienta HoverTool al gráfico
    hover = HoverTool(tooltips=[("Nombre", "@name"), ("ID HD", "@id1"),
                                ("ID HRN", "@id2"), ("Brillo", "@brightness")], renderers=[circles])
    fig.add_tools(hover)

    # Guardar el gráfico
    output_file("grafico.html")
    save(fig)
    
    # Guarda la figura en una imagen PNG
    export_png(fig, filename=f"{title_pic}.png")

def cargar_datos():
    # Leer el archivo y crear las listas de datos
    x_coords = []
    y_coords = []
    id_hd = []
    brillo = []
    id_hrn = []
    nombres = []

    with open("constellations/stars.txt", "r") as f:
        for line in f:
            data = line.split()
            x_coords.append(float(data[0]))
            y_coords.append(float(data[1]))
            id_hd.append(float(data[3]))
            brillo.append(float(data[4]))
            id_hrn.append(float(data[5]))

            if len(data) > 6:
                nom = ''
                for i in range(6, len(data)):
                    nom += " " + data[i]
                nombres.append(nom)
            else:
                nombres.append("")
        
        return [x_coords, y_coords, id_hd, brillo, id_hrn, nombres]


#Funcion para generar el gráfico de las estrellas cuando se requiera
def estrellas():
    datos = cargar_datos()
    x_coords = datos[0]
    y_coords = datos[1]
    id_hd = datos[2]
    brillo = datos[3]
    id_hrn = datos[4]
    nombres = datos[5]

    crear_grafico(x_coords, y_coords, nombres, id_hd, brillo, id_hrn,
                "Coordenadas de las estrellas", False, "Coordenadas estrellas")


#Funcion para generar el gráfico de las constelaciones cuando se requiera
def constelacion(conste):
    datos = cargar_datos()
    x_coords = datos[0]
    y_coords = datos[1]
    id_hd = datos[2]
    brillo = datos[3]
    id_hrn = datos[4]
    nombres = datos[5]

    stars = []

    with open(f"constellations/{conste}.txt", "r") as f:
        for line in f:
            data = line.split(",")
            stars.append(data[0])
            data[1] = data[1][:len(data[1])-1]
            stars.append(data[1])

    coords_x = []
    coords_y = []
    id_hd_cons = []
    brillo_cons = []
    id_hrn_cons = []

    for star in stars:
        for i in range(len(nombres)):
            if star in nombres[i]:
                coords_x.append(x_coords[i])
                coords_y.append(y_coords[i])
                id_hd_cons.append(id_hd[i])
                brillo_cons.append(brillo[i])
                id_hrn_cons.append(id_hrn[i])
    
    crear_grafico(coords_x, coords_y, stars, id_hd_cons, brillo_cons,
                id_hrn_cons, f"Constelación {conste}", True, "Constelacion")