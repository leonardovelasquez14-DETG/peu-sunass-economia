/**
 * Google Apps Script — Reseñas Públicas para Simulador PEU SUNASS (BackBone Academy)
 *
 * INSTRUCCIONES (2 minutos, una sola vez):
 * 1. Crea una hoja nueva en Google Sheets (ej. "Resenas_BackBone_SUNASS").
 * 2. Menú: Extensiones -> Apps Script.
 * 3. Borra el contenido por defecto, pega todo este archivo y guarda (Ctrl+S).
 * 4. Botón superior derecho: "Implementar" -> "Nueva implementación".
 *    - Tipo: "Aplicación web"
 *    - Ejecutar como: "Yo"
 *    - Quién tiene acceso: "Cualquier usuario"
 * 5. Autoriza los permisos y copia la "URL de la aplicación web" (termina en /exec).
 * 6. Pega esa URL en index.html en la constante REVIEWS_API_URL y haz push a GitHub.
 *
 * MODERACIÓN:
 * En tu hoja de Google Sheets verás la columna "visible" (SI / NO).
 * Para ocultar cualquier reseña no deseada, cambia "SI" por "NO" en esa fila.
 */

const SHEET_NAME = "Resenas";
const HEADERS = ["fecha", "nombre", "universidad", "rating", "comentario", "visible"];

function getOrCreateSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold");
  }
  return sheet;
}

function jsonOutput_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  try {
    const sheet = getOrCreateSheet_();
    const lastRow = sheet.getLastRow();
    if (lastRow < 2) {
      return jsonOutput_({ ok: true, reviews: [] });
    }
    const rows = sheet.getRange(2, 1, lastRow - 1, HEADERS.length).getValues();
    const reviews = [];
    for (let i = rows.length - 1; i >= 0; i--) {
      const [fecha, nombre, universidad, rating, comentario, visible] = rows[i];
      if (String(visible || "SI").trim().toUpperCase() !== "SI") continue;
      const r = parseInt(rating, 10);
      if (!nombre || !comentario || isNaN(r) || r < 1 || r > 5) continue;
      reviews.push({
        fecha: String(fecha || ""),
        nombre: String(nombre).slice(0, 60),
        universidad: String(universidad || "").slice(0, 80),
        rating: r,
        comentario: String(comentario).slice(0, 400)
      });
    }
    return jsonOutput_({ ok: true, reviews: reviews.slice(0, 100) });
  } catch (err) {
    return jsonOutput_({ ok: false, error: String(err) });
  }
}

function doPost(e) {
  try {
    const raw = (e && e.postData && e.postData.contents) ? e.postData.contents : "{}";
    const data = JSON.parse(raw);

    const nombre = String(data.nombre || "").trim().slice(0, 60);
    const universidad = String(data.universidad || "").trim().slice(0, 80);
    const comentario = String(data.comentario || "").trim().slice(0, 400);
    const rating = parseInt(data.rating, 10);

    if (nombre.length < 2) {
      return jsonOutput_({ ok: false, error: "Ingresa tu nombre (mínimo 2 caracteres)." });
    }
    if (comentario.length < 8) {
      return jsonOutput_({ ok: false, error: "Escribe una reseña de al menos 8 caracteres." });
    }
    if (isNaN(rating) || rating < 1 || rating > 5) {
      return jsonOutput_({ ok: false, error: "Calificación inválida (1 a 5 estrellas)." });
    }

    const now = Utilities.formatDate(new Date(), "America/Lima", "yyyy-MM-dd HH:mm");
    const sheet = getOrCreateSheet_();
    sheet.appendRow([now, nombre, universidad, rating, comentario, "SI"]);

    return jsonOutput_({
      ok: true,
      review: { fecha: now, nombre, universidad, rating, comentario }
    });
  } catch (err) {
    return jsonOutput_({ ok: false, error: String(err) });
  }
}
