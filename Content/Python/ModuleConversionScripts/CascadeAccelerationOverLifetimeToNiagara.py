from ModuleConverterInterface import ModuleConverterInterface
import unreal as ue
from unreal import FXConverterUtilitiesLibrary as ueFxUtils
import CascadeToNiagaraHelperMethods as c2nUtils
import Paths


class CascadeAccelerationOverLifetimeConverter(ModuleConverterInterface):

    @classmethod
    def get_input_cascade_module(cls):
        return ue.ParticleModuleAccelerationOverLifetime

    @classmethod
    def convert(cls, args):
        cascade_module = args.get_cascade_module()
        emitter = args.get_niagara_emitter_context()

        # find/add the module script for acceleration force
        script_asset = ue.AssetData(Paths.script_acceleration_force)
        script_args = ue.CreateScriptContextArgs(script_asset, [1, 0])
        acceleration_script = emitter.find_or_add_module_script(
            "Acceleration",
            script_args,
            ue.ScriptExecutionCategory.PARTICLE_UPDATE)

        # get all properties from the cascade acceleration module
        # noinspection PyTypeChecker
        acceleration_over_life = ueFxUtils.get_particle_module_acceleration_over_lifetime_props(cascade_module)

        # make an input to apply the acceleration vector
        acceleration_input = c2nUtils.create_script_input_for_distribution(acceleration_over_life)

        # set the acceleration value
        acceleration_script.set_parameter("Acceleration", acceleration_input)

        # make sure there is a solve forces and velocity module.
        script_asset = ue.AssetData(Paths.script_solve_forces_and_velocity)
        script_args = ue.CreateScriptContextArgs(script_asset)
        emitter.find_or_add_module_script(
            "SolveForcesAndVelocity",
            script_args,
            ue.ScriptExecutionCategory.PARTICLE_UPDATE)
