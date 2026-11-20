# -*- coding: utf-8 -*-
"""Guion del vídeo "GTA 6: TODO lo que tienes que saber" (≈20 min).

Cada escena = (visual, narración). El visual es un dict que interpreta visuals.py.
"""

S = []  # lista de escenas


def esc(visual, texto):
    S.append({"visual": visual, "texto": " ".join(texto.split())})


# ───────────────────────── 0. INTRO ─────────────────────────
esc({"t": "title", "title": "GTA VI", "sub": "TODO LO QUE TIENES QUE SABER", "bg": "sunset"},
    """Trece años. Trece años desde que Grand Theft Auto cinco llegó a las tiendas.
    Trece años de rumores, de filtraciones, de memes y de tráileres que rompieron internet.
    Y por fin, el diecinueve de noviembre de dos mil veintiséis, la espera terminó.""")
esc({"t": "scene", "bg": "skyline", "cap": "Bienvenidos a Leonida"},
    """Grand Theft Auto seis ya está aquí. Y no es un lanzamiento cualquiera:
    es, probablemente, el estreno más grande de la historia del entretenimiento.
    Más grande que cualquier película, que cualquier disco, que cualquier otro videojuego.""")
esc({"t": "bullets", "title": "EN ESTE VÍDEO", "items": [
    "13 años de espera", "Filtraciones y retrasos", "El mapa de Leonida",
    "Lucía y Jason", "Jugabilidad y tecnología", "Notas, ventas y récords", "¿Y ahora qué?"],
     "bg": "grid"},
    """En este vídeo vamos a repasarlo todo. De dónde viene este juego, por qué tardó tanto,
    cómo es el estado de Leonida, quiénes son Lucía y Jason, qué ha cambiado en la jugabilidad,
    y qué está pasando ahora mismo con las notas de la crítica y unas cifras de ventas
    que, sinceramente, cuesta creer. Ponte cómodo, porque esto va para largo.""")
esc({"t": "scene", "bg": "night", "cap": "Suscríbete y activa la campana"},
    """Y antes de empezar, si te gustan los vídeos largos y bien explicados sobre videojuegos,
    suscríbete al canal y activa la campana. Nos ayuda muchísimo. Ahora sí, vamos allá.""")

# ───────────────────────── 1. 13 AÑOS ─────────────────────────
esc({"t": "chapter", "n": "01", "title": "TRECE AÑOS DE ESPERA", "bg": "sunset"},
    """Capítulo uno. Trece años de espera.""")
esc({"t": "stat", "big": "2013", "label": "Llega GTA V", "sub": "17 de septiembre de 2013", "bg": "skyline"},
    """Para entender lo que significa GTA seis, hay que volver a dos mil trece.
    Ese septiembre, Rockstar lanzó Grand Theft Auto cinco en PlayStation tres y Xbox trescientos sesenta.
    Michael, Franklin y Trevor, la ciudad de Los Santos, y un juego que lo cambió todo.""")
esc({"t": "stat", "big": "+210 M", "label": "copias de GTA V", "sub": "Uno de los juegos más vendidos de la historia", "bg": "grid"},
    """GTA cinco se convirtió en uno de los productos de entretenimiento más rentables jamás creados.
    Ha superado las doscientas diez millones de copias vendidas, y salió en tres generaciones de consolas distintas:
    PlayStation tres, PlayStation cuatro, PlayStation cinco, y sus equivalentes en Xbox, además de PC.""")
esc({"t": "scene", "bg": "night", "cap": "GTA Online: la gallina de los huevos de oro"},
    """Pero el verdadero motor fue GTA Online. El modo multijugador generó miles de millones de dólares
    en microtransacciones durante más de una década. Y eso tuvo una consecuencia directa:
    Rockstar no tenía ninguna prisa por sacar una secuela. Mientras tanto, el estudio lanzó
    Red Dead Redemption dos en dos mil dieciocho, otra obra maestra, y los fans de GTA seguían esperando.""")
esc({"t": "timeline", "title": "EL CAMINO HASTA GTA VI", "events": [
    ("2013", "Sale GTA V"), ("2018", "Red Dead Redemption 2"), ("Feb 2022", "Rockstar confirma GTA VI"),
    ("Sep 2022", "Filtración masiva"), ("Dic 2023", "Tráiler 1"), ("May 2025", "Tráiler 2"),
    ("19 Nov 2026", "Lanzamiento")], "bg": "grid"},
    """Durante años, todo fueron rumores. Proyecto Americas, decían algunos. Que si volvería Vice City,
    que si habría protagonista femenina, que si el mapa cubriría varios países.
    Hasta que en febrero de dos mil veintidós, Rockstar por fin lo confirmó de forma oficial:
    el desarrollo del próximo Grand Theft Auto estaba, cito, muy avanzado.""")

# ───────────────────────── 2. FILTRACIÓN ─────────────────────────
esc({"t": "chapter", "n": "02", "title": "LA FILTRACIÓN", "bg": "night"},
    """Capítulo dos. La filtración que sacudió a la industria.""")
esc({"t": "stat", "big": "90", "label": "vídeos filtrados", "sub": "Septiembre de 2022", "bg": "night"},
    """En septiembre de dos mil veintidós ocurrió algo sin precedentes. Un hacker accedió a sistemas internos
    de Rockstar y publicó en un foro alrededor de noventa vídeos de una versión temprana de GTA seis.
    Animaciones a medio hacer, menús de depuración, texturas provisionales. Y, sobre todo,
    la confirmación de muchos rumores: Vice City volvía, y habría dos protagonistas, un hombre y una mujer.""")
esc({"t": "quote", "text": "Esta filtración no afectará al desarrollo a largo plazo.", "author": "Rockstar Games, 2022 (paráfrasis)", "bg": "night"},
    """La reacción de Rockstar fue sobria. Reconocieron la intrusión, dijeron que estaban
    profundamente decepcionados, y aseguraron que el desarrollo seguiría su curso.
    Muchos desarrolladores de todo el mundo salieron en su defensa, recordando a los jugadores
    que un juego en desarrollo siempre se ve mal, y que eso no dice nada del resultado final.""")
esc({"t": "scene", "bg": "highway", "cap": "Un adolescente detrás del hackeo"},
    """Más tarde se supo que detrás del ataque estaba un joven británico vinculado al grupo Lapsus,
    que ya había atacado a otras grandes empresas tecnológicas. El caso acabó en los tribunales.
    Y aunque fue un golpe duro para el estudio, tuvo un efecto inesperado: el interés por GTA seis
    se disparó todavía más.""")

# ───────────────────────── 3. TRÁILERS ─────────────────────────
esc({"t": "chapter", "n": "03", "title": "LOS TRÁILERES QUE ROMPIERON INTERNET", "bg": "sunset"},
    """Capítulo tres. Los tráileres que rompieron internet.""")
esc({"t": "stat", "big": "90 M", "label": "visualizaciones en 24 h", "sub": "Tráiler 1 · Diciembre de 2023", "bg": "sunset"},
    """En noviembre de dos mil veintitrés, Rockstar anunció que el primer tráiler llegaría en diciembre.
    Pero el cuatro de diciembre, horas antes de lo previsto, el vídeo se filtró en redes sociales.
    Rockstar reaccionó publicándolo de inmediato. En apenas veinticuatro horas, el tráiler superó las noventa millones
    de visualizaciones en YouTube, convirtiéndose en el vídeo no musical más visto en su primer día.""")
esc({"t": "scene", "bg": "beach", "cap": "Vice City, parodia de las redes sociales"},
    """El tráiler era una carta de amor a la Florida de los vídeos virales. Gente haciendo locuras en la playa,
    caimanes en las tiendas, fiestas en barcos, clubes nocturnos, y todo filtrado a través de pantallas verticales
    de móviles, como si fuera un feed de redes sociales. Era la sátira de Rockstar, actualizada a la era de los influencers.""")
esc({"t": "quote", "text": "Love Is a Long Road", "author": "Tom Petty · la canción del primer tráiler", "bg": "sunset"},
    """Y luego estaba la canción. Love Is a Long Road, de Tom Petty. Un tema de mil novecientos ochenta y nueve
    que, de repente, volvió a las listas de reproducción de todo el mundo. Y al final del tráiler,
    la escena que lo resumía todo: una pareja atracando una tienda juntos. Un Bonnie y Clyde moderno.""")
esc({"t": "stat", "big": "475 M", "label": "visualizaciones en 24 h", "sub": "Tráiler 2 · 6 de mayo de 2025 (según Rockstar)", "bg": "night"},
    """El segundo tráiler llegó por sorpresa el seis de mayo de dos mil veinticinco, pocos días después
    de anunciarse el primer retraso. Rockstar aseguró que sumó cuatrocientas setenta y cinco millones de visualizaciones
    en todas las plataformas durante sus primeras veinticuatro horas. Una cifra absurda.""")
esc({"t": "scene", "bg": "skyline", "cap": "Tráiler 2: la historia toma forma"},
    """Este segundo tráiler fue mucho más narrativo. Nos presentó en profundidad a Jason y a Lucía,
    mostró secuencias en tiempo real con una calidad visual que dejó a medio mundo con la boca abierta,
    y vino acompañado de una web oficial con decenas de capturas, descripciones de personajes y de zonas del mapa.
    Durante semanas, la comunidad analizó cada píxel.""")

# ───────────────────────── 4. RETRASOS ─────────────────────────
esc({"t": "chapter", "n": "04", "title": "LOS RETRASOS", "bg": "grid"},
    """Capítulo cuatro. Los retrasos.""")
esc({"t": "timeline", "title": "FECHAS DE LANZAMIENTO", "events": [
    ("Dic 2023", "Anunciado para 2025"), ("May 2025", "Retraso: 26 mayo 2026"),
    ("Nov 2025", "Retraso: 19 nov 2026"), ("19 Nov 2026", "¡Lanzamiento!")], "bg": "grid"},
    """Cuando se mostró el primer tráiler, la fecha prometida era dos mil veinticinco.
    Pero en mayo de dos mil veinticinco llegó el primer golpe: GTA seis se iba al veintiséis de mayo de dos mil veintiséis.
    Y en noviembre de ese mismo año, un segundo retraso lo empujó hasta el diecinueve de noviembre de dos mil veintiséis.""")
esc({"t": "quote", "text": "Necesitamos un poco más de tiempo para pulir el juego al nivel que esperáis.",
     "author": "Rockstar Games (paráfrasis)", "bg": "sunset"},
    """Rockstar justificó ambos retrasos con el mismo argumento: necesitaban tiempo extra para pulir el juego
    al nivel de calidad que los jugadores esperaban. Y aunque la comunidad se resignó entre memes,
    la industria entera reorganizó sus calendarios. Muchas editoras movieron sus propios lanzamientos
    para no coincidir con el gigante. Nadie quería competir con GTA seis.""")
esc({"t": "scene", "bg": "night", "cap": "La espera se convirtió en meme"},
    """Porque esto es otra cosa que GTA seis ha conseguido antes incluso de salir: convertirse en un fenómeno cultural.
    Hubo bromas sobre que saldría antes la colonización de Marte, comparaciones con otros acontecimientos históricos,
    y cuentas atrás por todas partes. La espera, en sí misma, se volvió parte de la experiencia.""")

# ───────────────────────── 5. LEONIDA ─────────────────────────
esc({"t": "chapter", "n": "05", "title": "BIENVENIDOS A LEONIDA", "bg": "beach"},
    """Capítulo cinco. Bienvenidos a Leonida.""")
esc({"t": "map", "title": "ESTADO DE LEONIDA", "hl": None, "bg": "map"},
    """El juego no se limita a una ciudad. Por primera vez desde San Andreas, el mapa es un estado entero:
    Leonida, la versión satírica que Rockstar hace de Florida. Y está dividido en varias regiones muy distintas entre sí.""")
esc({"t": "map", "title": "VICE CITY", "hl": "Vice City", "bg": "map"},
    """La joya de la corona es, por supuesto, Vice City. La ciudad que ya visitamos en dos mil dos,
    ambientada entonces en los años ochenta, vuelve ahora en su versión moderna.
    Rascacielos, playas, Ocean Drive con sus luces de neón, yates de lujo, y una vida nocturna que no se detiene.""")
esc({"t": "scene", "bg": "beach", "cap": "Vice City, hoy"},
    """La densidad de detalle es lo que más llama la atención. Cada calle está llena de gente,
    cada local tiene su interior, cada playa está repleta de turistas, culturistas, vendedores y personajes estrafalarios.
    Rockstar ha intentado que la ciudad se sienta viva de verdad, y no solo como un decorado.""")
esc({"t": "map", "title": "LEONIDA KEYS", "hl": "Leonida Keys", "bg": "map"},
    """Al sur están los Leonida Keys, una cadena de islas inspirada en los Cayos de Florida.
    Puentes infinitos sobre aguas turquesa, pueblos pesqueros, bares de carretera y, cómo no,
    contrabando. Aquí es donde empieza la historia de Jason.""")
esc({"t": "map", "title": "GRASSRIVERS", "hl": "Grassrivers", "bg": "map"},
    """Grassrivers es el equivalente a los Everglades. Pantanos enormes, hierba alta, aerodeslizadores y caimanes.
    Muchos caimanes. Es una de las zonas más salvajes del mapa, y promete persecuciones y escondites
    que no habíamos visto nunca en la saga.""")
esc({"t": "map", "title": "PORT GELLHORN", "hl": "Port Gellhorn", "bg": "map"},
    """Port Gellhorn representa la otra cara de Leonida: una ciudad costera venida a menos,
    con moteles baratos, centros comerciales abandonados y gente que intenta salir adelante como puede.
    Es la parte menos glamurosa del sueño americano.""")
esc({"t": "map", "title": "AMBROSIA", "hl": "Ambrosia", "bg": "map"},
    """Ambrosia es la zona agrícola e industrial. Campos de caña de azúcar, refinerías, pueblos pequeños
    y clubes de moteros. Un territorio duro, donde la ley no siempre llega.""")
esc({"t": "map", "title": "MOUNT KALAGA", "hl": "Mount Kalaga", "bg": "map"},
    """Y al norte, el Parque Nacional de Mount Kalaga: bosques, ríos, senderos, caza y pesca.
    Un espacio natural enorme que recuerda a lo que Rockstar consiguió con Red Dead Redemption dos,
    pero trasladado a la época actual.""")
esc({"t": "stat", "big": "x2", "label": "más grande que Los Santos", "sub": "Estimación de la comunidad", "bg": "map"},
    """¿Y cómo de grande es? Rockstar no ha dado cifras oficiales en kilómetros cuadrados, pero la comunidad,
    analizando tráileres y capturas, estima que el mapa es claramente mayor que el de GTA cinco.
    Y lo más importante: mucho más denso. Más interiores, más edificios accesibles y más cosas que hacer por metro cuadrado.""")

# ───────────────────────── 6. PROTAGONISTAS ─────────────────────────
esc({"t": "chapter", "n": "06", "title": "LUCÍA Y JASON", "bg": "sunset"},
    """Capítulo seis. Lucía y Jason.""")
esc({"t": "character", "name": "LUCÍA CAMINOS", "role": "Protagonista", "color": "pink", "bg": "sunset"},
    """Lucía Caminos es la primera protagonista femenina de la saga principal de Grand Theft Auto
    en la era moderna. Es latina, dura, y la conocemos en el primer tráiler en un lugar muy concreto:
    la Penitenciaría de Leonida.""")
esc({"t": "scene", "bg": "night", "cap": "Lucía: aprender a luchar"},
    """Su padre le enseñó a pelear desde que podía caminar. La vida le ha dado golpes desde entonces,
    y luchar por su familia la llevó a la cárcel. Cuando sale, tiene una idea clara:
    no va a cometer los mismos errores. Quiere una vida mejor, y está dispuesta a todo para conseguirla.""")
esc({"t": "character", "name": "JASON DUVAL", "role": "Protagonista", "color": "teal", "bg": "beach"},
    """Jason Duval es el otro protagonista. Creció rodeado de estafadores y delincuentes, se alistó en el ejército
    para intentar escapar de ese mundo, y acabó de vuelta en los Keys, haciendo lo único que sabe hacer:
    trabajar para traficantes locales.""")
esc({"t": "scene", "bg": "beach", "cap": "Jason: buscando una salida"},
    """Jason quiere una vida tranquila. Pero en Leonida, la tranquilidad es un lujo. Y cuando conoce a Lucía,
    todo cambia. Quizá sea lo mejor que le ha pasado. O quizá lo peor.""")
esc({"t": "quote", "text": "Solo podemos salir de esto si confiamos el uno en el otro.",
     "author": "La premisa de GTA VI, en una frase", "bg": "sunset"},
    """La relación entre los dos es el corazón de la historia. A diferencia de GTA cinco, donde Michael, Franklin y Trevor
    eran tres hombres con agendas propias, aquí tenemos una pareja. Una historia de amor y de crimen,
    donde la confianza es la moneda más valiosa. Y donde, según el propio tráiler,
    todo se tuerce cuando un golpe sencillo sale mal.""")
esc({"t": "scene", "bg": "highway", "cap": "Cambio entre protagonistas"},
    """Como en GTA cinco, podemos alternar entre los dos personajes en muchos momentos, y la historia
    va saltando entre sus puntos de vista. Pero esta vez su vínculo emocional es mucho más fuerte,
    y eso cambia el tono de toda la narrativa.""")

# ───────────────────────── 7. SECUNDARIOS ─────────────────────────
esc({"t": "chapter", "n": "07", "title": "EL REPARTO DE LEONIDA", "bg": "night"},
    """Capítulo siete. El reparto de Leonida.""")
esc({"t": "character", "name": "CAL HAMPTON", "role": "El amigo de Jason", "color": "orange", "bg": "beach"},
    """Alrededor de Lucía y Jason gira un reparto lleno de personajes muy de Rockstar.
    Cal Hampton es el mejor amigo de Jason. Pasa el día en casa, enganchado a internet y convencido
    de que el gobierno le vigila. Teorías conspirativas, cerveza y radioaficionado.
    Probablemente el alivio cómico de la historia.""")
esc({"t": "character", "name": "BOOBIE IKE", "role": "Leyenda de Vice City", "color": "purple", "bg": "night"},
    """Boobie Ike es una leyenda local de Vice City. Empezó en la calle y ahora es dueño de negocios inmobiliarios,
    un club de striptease y un sello discográfico, Only Raw Records. Un empresario que sabe que,
    en esta ciudad, todo el mundo tiene un precio.""")
esc({"t": "character", "name": "DRE'QUAN PRIEST", "role": "Only Raw Records", "color": "pink", "bg": "night"},
    """Dre'Quan Priest trabaja para Boobie y quiere convertirse en un gran productor musical.
    Su gran apuesta son Real Dimez, un dúo de raperas que se hizo viral años atrás y que busca
    volver a lo más alto. La música, como siempre en GTA, tiene un papel muy importante.""")
esc({"t": "character", "name": "RAUL BAUTISTA", "role": "Atracador veterano", "color": "teal", "bg": "highway"},
    """Raúl Bautista es un atracador de bancos con mucha experiencia, carismático y peligroso.
    Siempre busca nuevos talentos para sus golpes, y ve en Jason y Lucía una oportunidad.
    Aunque, como todo en Leonida, nunca sabes cuánto puedes fiarte.""")
esc({"t": "character", "name": "BRIAN HEDER", "role": "Contrabandista de los Keys", "color": "orange", "bg": "beach"},
    """Y Brian Heder es un viejo contrabandista de los Keys, que lleva décadas moviendo mercancía por la costa.
    Deja que Jason viva en una de sus propiedades, a cambio de, digamos, algunos favores.""")

# ───────────────────────── 8. JUGABILIDAD ─────────────────────────
esc({"t": "chapter", "n": "08", "title": "JUGABILIDAD Y TECNOLOGÍA", "bg": "grid"},
    """Capítulo ocho. Jugabilidad y tecnología.""")
esc({"t": "bullets", "title": "NOVEDADES CLAVE", "items": [
    "Iluminación y reflejos de nueva generación", "Multitudes mucho más densas",
    "Interiores accesibles en todo el mapa", "Física de agua y vehículos renovada",
    "Animaciones heredadas de RDR2", "Redes sociales dentro del juego"], "bg": "grid"},
    """Técnicamente, GTA seis es una bestia. El motor de Rockstar, RAGE, ha dado un salto enorme.
    La iluminación global, los reflejos, la vegetación, el agua y los efectos meteorológicos
    están a otro nivel. Y las multitudes: cientos de personajes en pantalla, cada uno con sus propias rutinas.""")
esc({"t": "scene", "bg": "skyline", "cap": "La herencia de Red Dead Redemption 2"},
    """Mucho de lo aprendido en Red Dead Redemption dos se ha trasladado aquí. Las animaciones son más pesadas y realistas,
    los personajes interactúan con el entorno de forma más creíble, y los NPC reaccionan a lo que haces
    de una manera mucho más natural. Si empujas a alguien, se acuerda. Si conduces como un loco, la gente lo graba con el móvil.""")
esc({"t": "scene", "bg": "night", "cap": "Las redes sociales como mecánica"},
    """Y eso nos lleva a una de las grandes ideas del juego: las redes sociales. Leonida está obsesionada con grabarlo todo.
    Los vídeos virales, los directos y los influencers forman parte del mundo, y la sátira de Rockstar apunta directamente
    a la cultura digital de hoy en día.""")
esc({"t": "scene", "bg": "highway", "cap": "Conducción, armas y policía"},
    """En cuanto a la conducción, los coches tienen más peso y mejores daños. El sistema de búsqueda policial es más inteligente,
    con agentes que investigan, que buscan testigos y que no se limitan a perseguirte en línea recta.
    Y los atracos, el gran tema del juego, vuelven con planificación, roles y decisiones.""")
esc({"t": "stat", "big": "30 FPS", "label": "objetivo en consola", "sub": "Según los análisis publicados", "bg": "grid"},
    """Eso sí, no todo es perfecto. Según varios análisis, en consolas el juego apunta a treinta fotogramas por segundo,
    priorizando la fidelidad visual. Hay quien lo considera una decisión razonable dada la escala del mundo,
    y quien lo ve como el principal punto débil técnico. Es el eterno debate.""")
esc({"t": "scene", "bg": "sunset", "cap": "Solo en consolas... por ahora"},
    """Además, como pasó con GTA cinco y con Red Dead dos, el juego ha salido solo en PlayStation cinco y Xbox Series.
    De la versión de PC, de momento, no hay fecha. Los jugadores de ordenador, una vez más, tendrán que esperar.""")

# ───────────────────────── 9. LANZAMIENTO ─────────────────────────
esc({"t": "chapter", "n": "09", "title": "EL LANZAMIENTO", "bg": "sunset"},
    """Capítulo nueve. El lanzamiento.""")
esc({"t": "stat", "big": "19.11.2026", "label": "Día de lanzamiento", "sub": "PlayStation 5 · Xbox Series X|S", "bg": "night"},
    """Y llegamos al momento clave. El diecinueve de noviembre de dos mil veintiséis, GTA seis salió a la venta
    en PlayStation cinco y Xbox Series. Las precargas se abrieron unos días antes, el diez de noviembre,
    y la descarga en PlayStation rondaba los doscientos diez gigas. Así que más vale que tuvieras espacio libre.""")
esc({"t": "stat", "big": "80 $", "label": "Edición estándar", "sub": "Edición superior: ~100 $", "bg": "grid"},
    """El precio fue uno de los temas más discutidos de los meses previos. Finalmente, la edición estándar
    se situó en torno a los ochenta dólares, con una edición superior cercana a los cien.
    Un precio alto, que reabre el debate sobre el coste de los videojuegos. Aunque, a juzgar por las ventas,
    no parece haber frenado a casi nadie.""")
esc({"t": "stat", "big": "99", "label": "Metacritic", "sub": "Empata con el récord histórico", "bg": "sunset"},
    """Porque, vamos con las notas. GTA seis ha aterrizado con un noventa y nueve en Metacritic. Esa cifra empata
    con el récord histórico que hasta ahora tenía en solitario The Legend of Zelda: Ocarina of Time.
    Y con una diferencia: la de GTA seis se calcula sobre más de cien análisis, frente a poco más de veinte de Ocarina.""")
esc({"t": "bullets", "title": "LO QUE DICE LA CRÍTICA", "items": [
    "+ Un mundo abierto sin rival", "+ Historia y personajes memorables", "+ Nivel técnico apabullante",
    "– Arranque lento en las primeras horas", "– 30 FPS en consola"], "bg": "grid"},
    """Los análisis coinciden en lo esencial: el mundo abierto más detallado jamás creado, una historia madura
    con dos personajes muy bien escritos, y un nivel técnico que marca una nueva referencia.
    Las críticas, que las hay, apuntan sobre todo a un arranque lento, con unas primeras horas muy pausadas,
    y al rendimiento en consola.""")
esc({"t": "stat", "big": "3.790 M $", "label": "ventas del primer día", "sub": "Cifra comunicada por la compañía", "bg": "night"},
    """Y luego están las ventas. Según la propia compañía, GTA seis habría generado unos tres mil setecientos noventa millones
    de dólares en ventas el primer día. Si se confirma, sería el mayor lanzamiento de la historia del entretenimiento,
    muy por encima de cualquier estreno de cine.""")
esc({"t": "stat", "big": "2.360 M $", "label": "estimación independiente", "sub": "Sensor Tower · ~24,5 M de copias", "bg": "grid"},
    """Ahora bien, hay que ser prudentes. Esas cifras son estimaciones internas, y otras fuentes independientes, como Sensor Tower,
    hablan de unos dos mil trescientos sesenta millones de dólares y alrededor de veinticuatro millones y medio de copias
    entre reservas y primer día. Aun así, estamos hablando de números sin precedentes. Sea cual sea la cifra exacta,
    es un récord.""")
esc({"t": "scene", "bg": "night", "cap": "La noche en que cayó PlayStation Network"},
    """El lanzamiento tampoco estuvo libre de caos. La noche del estreno, la PlayStation Network sufrió problemas
    por la avalancha de jugadores intentando descargar y activar el juego al mismo tiempo. Y en las plataformas de streaming,
    millones de personas se conectaron simultáneamente para ver a sus creadores favoritos dar sus primeros pasos por Leonida,
    batiendo récords de audiencia para un solo juego.""")

# ───────────────────────── 10. FUTURO ─────────────────────────
esc({"t": "chapter", "n": "10", "title": "¿Y AHORA QUÉ?", "bg": "grid"},
    """Capítulo diez. ¿Y ahora qué?""")
esc({"t": "scene", "bg": "skyline", "cap": "El nuevo GTA Online"},
    """La gran pregunta es el futuro online. Si GTA Online fue la base del éxito de GTA cinco durante más de diez años,
    todo apunta a que Rockstar tiene planes ambiciosos para el multijugador de GTA seis. Un Leonida compartido,
    con negocios, atracos cooperativos y actualizaciones constantes, podría mantener vivo este juego durante otra década.""")
esc({"t": "scene", "bg": "sunset", "cap": "La versión de PC"},
    """También queda pendiente la versión de PC. Si la historia se repite, podría llegar uno o dos años después,
    con mejoras gráficas, más fotogramas por segundo y, por supuesto, una comunidad de mods que se frota las manos.""")
esc({"t": "scene", "bg": "highway", "cap": "Un antes y un después para la industria"},
    """Y por último, el impacto en la industria. GTA seis demuestra que los grandes lanzamientos todavía pueden paralizar el mundo.
    Que un juego para un solo jugador, con una historia cuidada, puede ser el producto cultural más esperado de una década.
    Pero también plantea preguntas: sobre los precios, sobre los ciclos de desarrollo de más de diez años,
    y sobre las condiciones de trabajo detrás de proyectos de este tamaño.""")

# ───────────────────────── 11. CONCLUSIÓN ─────────────────────────
esc({"t": "chapter", "n": "11", "title": "CONCLUSIÓN", "bg": "sunset"},
    """Capítulo once. Conclusión.""")
esc({"t": "scene", "bg": "beach", "cap": "¿Ha merecido la pena la espera?"},
    """Entonces, ¿ha merecido la pena esperar trece años? Si nos fiamos de la crítica y de los jugadores,
    la respuesta parece un sí rotundo. GTA seis no es solo una secuela: es la culminación de todo lo que Rockstar ha aprendido
    en más de veinticinco años haciendo mundos abiertos.""")
esc({"t": "scene", "bg": "sunset", "cap": "Lucía y Jason te esperan"},
    """Vice City ha vuelto, más brillante, más ruidosa y más absurda que nunca. Lucía y Jason nos esperan.
    Y Leonida, ese reflejo deformado de nuestra propia época, está lista para ser explorada.""")
esc({"t": "bullets", "title": "Y TÚ, ¿QUÉ OPINAS?", "items": [
    "¿Ya lo estás jugando?", "¿Te parece justo el precio?", "¿Lucía o Jason?",
    "Déjalo en los comentarios"], "bg": "grid"},
    """Y ahora quiero saber tu opinión. ¿Ya lo estás jugando? ¿Te parece justo su precio?
    ¿Con quién te quedas, con Lucía o con Jason? Déjamelo en los comentarios, que los leo todos.""")
esc({"t": "title", "title": "GRACIAS POR VER", "sub": "SUSCRÍBETE · LIKE · CAMPANA", "bg": "sunset"},
    """Si el vídeo te ha gustado, dale a me gusta, suscríbete al canal y activa la campana para no perderte
    los próximos vídeos, porque vamos a hablar mucho de GTA seis en las próximas semanas: guías, secretos y curiosidades.
    Muchas gracias por llegar hasta aquí. Nos vemos en el próximo vídeo. ¡Hasta pronto!""")

ESCENAS = S

if __name__ == "__main__":
    w = sum(len(e["texto"].split()) for e in S)
    print(len(S), "escenas,", w, "palabras")
