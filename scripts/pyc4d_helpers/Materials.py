import c4d
import pyc4d_helpers.Dictionaries as D
import pyc4d_helpers.UserData as ud

def CreateShader(shaderType, name="Shader"):

	"""
		Creates a new C4D Shader.
		Args:
			shaderType: The type of the shader. See https://github.com/GeorgeAdamon/pyc4d_helpers/blob/master/useful_tables/Shader%20Types.md
			[optional] name (str): The name of the Shader.
		Returns:
		The shader if succesful, else None
	"""
	shader = c4d.BaseList2D(shaderType)
	shader.SetName(name)

	return shader

def ApplyShader(shader, material, channel=c4d.MATERIAL_COLOR_SHADER):

	"""
		Applies a C4D shader on the specified channel of a C4D Material
		
		Args:
			shader: The Shader object to apply.
			material: The Material to apply the Shader to.
			channel: The Channel of the Material into which to apply the shader. See https://github.com/GeorgeAdamon/pyc4d_helpers/blob/master/useful_tables/Material%20Shader%20Channels.md
		Returns:
			True on success
	"""

	if isinstance(channel,str):
		channel = D.ShaderChannels[channel]

	material[channel] = shader
	material.InsertShader(shader)
	return True

	#mat.Message(c4d.MSG_UPDATE)
	#mat.Update(True, True)

def CreateMaterial(name="New Material", active_channels=[c4d.CHANNEL_COLOR]):

	"""
		Creates a new C4D Material, enabling the specified channels. This function does not insert the material
		into the C4D document. For this, do 'doc.InsertMaterial(mat)' , where 'mat' is the newly created Material
		returned bt this function.

		Args:
			[optional] name (str): The name of the material
			[optional] active_channels (list): A list of C4D channel types to enable.
		Returns:
			The newly created Material
	"""

	_mat = c4d.Material()
	_mat.SetName(name)

	for c in D.MaterialChannels.values():
		if c in active_channels:
			_mat.SetChannelState(c,True)
		else:
			_mat.SetChannelState(c,False)

	return _mat

def ApplyMaterial(obj, material, tagName, overwrite=False):

	"""
		Attaches a C4D material to a C4D object, by creating a new TextureTag.
	
		Args:
			obj: The object to attach the material to.
			material: The material to attach to the object.
			[optional] tagName (str): The name of the TextureTag.
			[optional] overwrite: If a textureTag is already present, should this function add a new textureTag, or use the existing one?
		Returns:
			True on success
	"""

	if obj==None: return False
	if material==None: return False
	if tagName==None: return False

	if overwrite == True:
		tags = obj.GetTags()
		for t in tags:
			if t.GetType()== c4d.Ttexture:
				t.SetMaterial(material)
				return t

	_tag = c4d.TextureTag()
	_tag.SetMaterial(material)
	_tag.SetName(tagName)
	obj.InsertTag(_tag)

	return _tag