from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CiudadForm
import requests


class ClimaBuscarView(LoginRequiredMixin, FormView):
    template_name = "clima/buscar.html"
    form_class = CiudadForm

    def form_valid(self, form):
        ciudad = form.cleaned_data["ciudad"]


        url_geo = "https://geocoding-api.open-meteo.com/v1/search"
        r_geo = requests.get(
            url_geo,
            params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
            timeout=12,
        )
        data_geo = r_geo.json()

        if not data_geo.get("results"):
            return render(self.request, "clima/resultados.html", {"error": f"No se encontró '{ciudad}'."})

        lat = data_geo["results"][0]["latitude"]
        lon = data_geo["results"][0]["longitude"]

      
        url_fc = "https://api.open-meteo.com/v1/forecast"
        r_fc = requests.get(
            url_fc,
            params={"latitude": lat, "longitude": lon, "current_weather": "true"},
            timeout=12,
        )
        clima = (r_fc.json() or {}).get("current_weather", {})

        return render(self.request, "clima/resultados.html", {"ciudad": ciudad, "clima": clima})

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})

class TopCiudadesView(LoginRequiredMixin, TemplateView):
    template_name = "clima/top.html"

    # Coordenadas fijas para evitar geocoding en lote
    CIUDADES = [
        {"nombre": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
        {"nombre": "Madrid", "lat": 40.4168, "lon": -3.7038},
        {"nombre": "Ciudad de México", "lat": 19.4326, "lon": -99.1332},
        {"nombre": "Bogotá", "lat": 4.7110, "lon": -74.0721},
        {"nombre": "Santiago", "lat": -33.4489, "lon": -70.6693},
        {"nombre": "Lima", "lat": -12.0464, "lon": -77.0428},
        {"nombre": "Montevideo", "lat": -34.9011, "lon": -56.1645},
        {"nombre": "Quito", "lat": -0.1807, "lon": -78.4678},
        {"nombre": "Asunción", "lat": -25.2637, "lon": -57.5759},
        {"nombre": "Caracas", "lat": 10.4806, "lon": -66.9036},
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        url_fc = "https://api.open-meteo.com/v1/forecast"
        ciudades_data = []
        for c in self.CIUDADES:
            try:
                r = requests.get(
                    url_fc,
                    params={
                        "latitude": c["lat"],
                        "longitude": c["lon"],
                        "current_weather": "true",
                    },
                    timeout=10,
                )
                cw = (r.json() or {}).get("current_weather", {})
            except Exception:
                cw = {}
            ciudades_data.append(
                {
                    "nombre": c["nombre"],
                    "lat": c["lat"],
                    "lon": c["lon"],
                    "clima": cw,
                }
            )
        ctx["ciudades"] = ciudades_data
        return ctx
