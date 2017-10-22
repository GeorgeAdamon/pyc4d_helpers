import c4d

FloatInterface = {
"Float":c4d.CUSTOMGUI_REAL,
"Float Slider": c4d.CUSTOMGUI_REALSLIDER,
"Float Slider No EditField": c4d.CUSTOMGUI_REALSLIDERONLY
}

FloatUnits = {
"Real":c4d.DESC_UNIT_FLOAT,
"Percent": c4d.DESC_UNIT_PERCENT,
"Degrees": c4d.DESC_UNIT_DEGREE,
"Meters": c4d.DESC_UNIT_METER
}

IntegerInterface = {
"Cycle":c4d.CUSTOMGUI_CYCLE,
"Cycle Button": c4d.CUSTOMGUI_CYCLEBUTTON,
"Integer":c4d.CUSTOMGUI_LONG,
"Integer Slider": c4d.CUSTOMGUI_LONGSLIDER
}

ScriptingContexts = {
1023866: "Python Generator",
1022749: "Python Tag",
1025800: "Python Effector"
}

ShaderChannels = {
"Color": c4d.MATERIAL_COLOR_SHADER,
"Diffusion": c4d.MATERIAL_DIFFUSION_SHADER,
"Luminance": c4d.MATERIAL_LUMINANCE_SHADER,
"Transparency": c4d.MATERIAL_TRANSPARENCY_SHADER,
"Reflectance": c4d.MATERIAL_REFLECTION_SHADER,
"Environment": c4d.MATERIAL_ENVIRONMENT_SHADER,
"Bump": c4d.MATERIAL_BUMP_SHADER,
"Normal": c4d.MATERIAL_NORMAL_SHADER,
"Alpha": c4d.MATERIAL_ALPHA_SHADER,
"Displacement": c4d.MATERIAL_DISPLACEMENT_SHADER
}

MaterialChannels = {
"Color": c4d.CHANNEL_COLOR,
"Diffusion": c4d.CHANNEL_DIFFUSION,
"Luminance": c4d.CHANNEL_LUMINANCE,
"Transparency": c4d.CHANNEL_TRANSPARENCY,
"Reflectance": c4d.CHANNEL_REFLECTION,
"Environment": c4d.CHANNEL_ENVIRONMENT,
"Fog": c4d.CHANNEL_FOG,
"Bump": c4d.CHANNEL_BUMP,
"Normal": c4d.CHANNEL_NORMAL,
"Alpha": c4d.CHANNEL_ALPHA,
"Glow": c4d.CHANNEL_GLOW,
"Displacement": c4d.CHANNEL_DISPLACEMENT
}