library(httr)   
library(sf)          
library(dyplr)
library(RColorBrewer) 
url <- "https://vmarcgis01.bucaramanga.gov.co/waserver/rest/services/LIMITES_POLITICOS/Barrios/FeatureServer/0/query?where=1%3D1&outFields=COD_COMUNA,NOMBRE_BAR,NOMBRE_ENT&f=geojson"
response <- GET(url)
temp_file <- tempfile(fileext = ".geojson")
writeBin(content(response, "raw"), temp_file)
mapa_bucaramanga <- st_read(temp_file)
print(mapa_bucaramanga)
df_filtrado <- df %>%
  filter(`BARRIO_VER shp` != "SIN INFORMACION")

df_filtrado <- df_filtrado %>%
  mutate(
    codigo_comuna = sub("\\..*", "", `COMUNA shp`), 
    nombre_comuna = sub("^[^.]*\\.\\s*", "", `COMUNA shp`) 
  )

mapa_bucaramanga_relacionado <- left_join(mapa_bucaramanga, df_filtrado, by = c("NOMBRE_BAR" = "BARRIO_VER shp"))

mapa_bucaramanga_relacionado <- mapa_bucaramanga_relacionado %>%
  filter(!is.na(clasfinal))
pal <- colorFactor(
  palette = c("red", "black", "lightblue"), 
  domain = mapa_bucaramanga_relacionado$clasfinal
)
leaflet(mapa_bucaramanga_relacionado) %>%
  addProviderTiles("CartoDB.Positron") %>%
  addPolygons(
    fillColor = ~pal(clasfinal),   
    color = "black",               
    weight = 0.2,                
    fillOpacity = 0.7,             
    popup = ~paste("Barrio: ", NOMBRE_BAR, "<br>Tipo de dengue: ", clasfinal), 
    highlightOptions = highlightOptions(weight = 3, color = "white", fillOpacity = 0.7)  
  ) %>%
  addLegend(
    position = "topright", 
    pal = pal, 
    values = mapa_bucaramanga_relacionado$clasfinal,
    title = "Tipos de Dengue",
    opacity = 1,
    labels = c("Dengue Grave", "Con Signos de Alarma", "Sin Signos de Alarma") 
)