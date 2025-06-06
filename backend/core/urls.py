from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from administracao.apis  import router as administracaoRouter
from webscrapping.apis import router as webscrappingRouter
api = NinjaAPI(
    title='API DO LUCAS',
    version="1.0.0",
    description="API para serem usadas no frontend"
)
api.add_router("/administracao", administracaoRouter)
api.add_router("/webscrapping", webscrappingRouter)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

