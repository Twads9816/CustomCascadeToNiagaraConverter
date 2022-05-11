from ModuleConverterInterface import ModuleConverterInterface
import unreal as ue
from unreal import FXConverterUtilitiesLibrary as ueFxUtils
import CascadeToNiagaraHelperMethods as c2nUtils


class CascadeMeshRotationRateMultiplyLifeConverter(ModuleConverterInterface):

    @classmethod
    def get_input_cascade_module(cls):
        return ue.ParticleModuleMeshRotationRateMultiplyLife

    @classmethod
    def convert(cls, args):
        cascade_module = args.get_cascade_module()
        emitter = args.get_niagara_emitter_context()
        
        # get all properties of the mesh rotation rate muliply life module.
        # noinspection PyTypeChecker
        life_multiplier_distribution = ueFxUtils.get_particle_module_mesh_rotation_rate_multiply_life_props(
            cascade_module)

        # create an input for the rotation rate scale.
        life_multiplier_input = c2nUtils.create_script_input_for_distribution(life_multiplier_distribution)

        #  todo handle rotation rate as euler
