# Documento de Diseño

Este juego es una especie de combinación entre un roguelike y un juego de plataformas en el que se trata de derrocar enemigos que compondrán los diferentes niveles y así finalizar victorioso de la aventura.

Con este juego tratamos de, a parte de aprobar la asignatura claramente, darle al usuario una experiencia al completa en la medida de lo posible a partir de la jugabilidad y los elementos audiovisuales que conforman el videojuego.

## Backstory
Viviremos la aventura de Chris, un guerrero de la tierra medieval que se encuentra atrapado en una mazmorra repleta de monstruos que buscan acabar con él y su objetivo es avanzar a través de ella derrotándolos para escapar.

En este camino, a medida que vamos derrocando a los distintos enemigos podremos ir desbloqueando diferentes objetos o armas para poder avanzar más facilmente, o no.

## Desarrollo del juego
El juego se desarrolla dentro de mazmorras cerradas en las cuales el protagonista va a encontrar diferentes enemigos que van a tratar de derrotarlo para que no pueda escapar de la prisión.

Se compone de un total de 6 clases de enemigos. 3 de ellos son considerados enemigos normales (Enemigo1, Enemigo2 y Enemigo3), los cuales dependiendo del nivel de dificultad que se haya seleccionado (Fácil, Normal o Difícil) aparecerán en mayor o menor número para tratar de impedir el avance. Será estrictamente necesario derrotar a todos los enemigos presentes en una habitación para que las puertas se desbloqueen y permitan el paso a la siguiente sala.

Al superar los desafíos ordinarios, se le proporcionarán al protagonista nuevos objetos y recompensas que le ayudarán a superar las siguientes pruebas. Además de estos enemigos que a priori son más fáciles de superar, se encuentran los Bosses (Boss1, Boss2 y Boss3), únicos, significativamente más difíciles de vencer y equipados con una mayor cantidad de puntos de vida que el resto de los personajes.
