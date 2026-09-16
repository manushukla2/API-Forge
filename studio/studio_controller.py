from core.ai.requirement_analyzer import RequirementAnalyzer
from core.ai.stack_recommender import StackRecommender
from core.ai.boilerplate_generator import BoilerplateGenerator
from core.developer.swagger_generator import SwaggerGenerator
from core.developer.project_scaffolder import ProjectScaffolder
from core.developer.api_contract_builder import APIContractBuilder


class StudioController:
    def __init__(self):
        self.req_analyzer    = RequirementAnalyzer()
        self.stack_recommender = StackRecommender()
        self.boilerplate_gen = BoilerplateGenerator()
        self.swagger_gen     = SwaggerGenerator()
        self.scaffolder      = ProjectScaffolder()
        self.contract_builder = APIContractBuilder()

    def run_full_pipeline(
        self,
        requirements: str,
        on_progress: callable = None
    ) -> dict:

        # Step 1 — Requirements analyze karo
        self._emit(on_progress, "Analyzing requirements...", 10)
        req_data = self.req_analyzer.analyze(requirements)

        # Step 2 — Stack recommend karo
        self._emit(on_progress, "Recommending tech stack...", 30)
        stack = self.stack_recommender.recommend(requirements)

        # Step 3 — Boilerplate generate karo
        self._emit(on_progress, "Generating boilerplate structure...", 50)
        boilerplate = self.boilerplate_gen.generate(stack, req_data)

        # Step 4 — API contract banao
        self._emit(on_progress, "Building API contract...", 70)
        contract = self.contract_builder.build(req_data)

        # Step 5 — Swagger spec generate karo
        self._emit(on_progress, "Generating OpenAPI spec...", 85)
        swagger_spec = self.swagger_gen.generate({
            "title":     req_data.get("project_name", "Generated API"),
            "version":   "1.0.0",
            "base_url":  "https://api.example.com",
            "endpoints": req_data.get("suggested_endpoints", [])
        })

        # Step 6 — FastAPI code generate karo
        self._emit(on_progress, "Generating FastAPI code...", 95)
        fastapi_code = self.swagger_gen.generate_fastapi_code(swagger_spec)

        self._emit(on_progress, "Done!", 100)

        return {
            "requirements":  req_data,
            "stack":         stack,
            "boilerplate":   boilerplate,
            "contract":      contract,
            "swagger_spec":  swagger_spec,
            "fastapi_code":  fastapi_code
        }

    def _emit(self, callback, message: str, progress: int):
        if callback:
            callback(message, progress)
