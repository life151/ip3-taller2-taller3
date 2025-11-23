import { cargarUsuarios } from "./usuarios.js";
import { cargarPeliculas, mostrarFormularioPelicula } from "./peliculas.js";
import { cargarFavoritos, mostrarFormularioFavorito } from "./favoritos.js";
import { cargarEstadisticas } from "./estadisticas.js";

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("nav-usuarios").addEventListener("click", cargarUsuarios);
  document.getElementById("nav-peliculas").addEventListener("click", cargarPeliculas);
  document.getElementById("nav-favoritos").addEventListener("click", cargarFavoritos);
  document.getElementById("nav-agregar-pelicula").addEventListener("click", mostrarFormularioPelicula);
  document.getElementById("nav-agregar-favorito").addEventListener("click", mostrarFormularioFavorito);
  document.getElementById("nav-estadisticas").addEventListener("click", cargarEstadisticas);
});