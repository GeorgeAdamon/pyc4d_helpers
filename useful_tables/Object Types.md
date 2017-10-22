# List of Cinema4d BaseObject types

Retrieved from https://developers.maxon.net/docs/Cinema4DPythonSDK/html/types/objects.html
Valid up to C4D version R18.
____

Cinema4D BaseObjects are Initiated in the following way:
	``` python
	new_object = c4d.BaseObject ( object_type )
	```

For example creating a cube from scratch, would be like:
	``` python
	obj = c4d.BaseObject(c4d.Ocube)
	```
____

## BaseObject Types

### Generic BaseObjects (not appearing in C4D GUI)
|BaseObject Type (SDK name) 	| Common name		|
|:------------------------------| :-----------------------------------: |
| 	__Obase__ 		|	_Base Object_ 		
| 	__Obasedeform__ 	|	_Base Deform Object_ 	
|	__Opoint__		|	_Point object_
|	__Obaseeffector__	|	_Base effector object_
|	__Obasemogen__		|	_Base mogen object_

### Primitive Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
|	__Ocapsule__		|	_Capsule Object_
|	__Ocone__		|	_Cone Object_		
|	__Ocube__		|	_Cube Object_	
|	__Ocylinder__		|	_Cylinder Object_
|	__Odisc__		|	_Disc Object_	
|	__Ofigure__		|	_Figure object_	
|	__Onull__		|	_Null object_
|	__Ooiltank__		|	_Oil-tank object_
|	__Oplane__		|	_Plane object_
|	__Oplatonic__		|	_Platonic object_
|	__Opolygon__		|	_Polygon object_
|	__Opyramid__		|	_Pyramid object_
|	__Orelief__		|	_Relief object_
|	__Osinglepoly__		|	_Single polygon object_
|	__Osphere__		| 	_Sphere object_
|	__Otorus__		|	_Torus object_
|	__Otube__		|	_Tube object_

### Spline Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
|	__Oline__		|	_Line_		
|	__Ospline__		|	_Spline object_
|	__Ospline4side__	|	_4-sided spline object_
|	__Osplinearc__		|	_Arc spline object_
|	__Osplinecircle__	|	_Circle spline object_
|	__Osplinecissoid__	|	_Cissoid spline object_
|	__Osplinecogwheel__	|	_Wheel spline object_
|	__Osplinecontour__	|	_Contour spline object_
|	__Osplinecycloid__	|	_Cycloid spline object_
|	__Osplineflower__	|	_Flower spline object_
|	__Osplineformula__	|	_Formula spline object_
|	__Osplinehelix__	|	_Helix spline object_
|	__Osplinenside__	|	_N-sided spline object_
|	__Osplineprimitive__	|	_Spline primitive_
|	__Osplineprofile__	|	_Profile spline object_
|	__Osplinerectangle__	|	_Rectangle spline object_
|	__Osplinestar__		|	_Star spline object_
|	__Osplinetext__		|	_Text spline object_

### Generator Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
| 	__Oarray__	 	|	_Array_ 			
| 	__Oatomarray__ 		| 	_Atom Array_ 		
|	__Oboole__		|	_Boolean_	
|	__Oinstance__		|	_Instance_		
|	__Ometaball__		|	_Metaball_
|	__Osymmetry__		|	_Symmetry object_

### Subdivision Surface Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
| 	__Obezier__		|	_Bezier Subdivision Surface_
|	__Oextrude__		|	_Extrude Subdivision Surface_	
|	__Olathe__		|	_Lathe Subdivision Surface_	
|	__Oloft__		|	_Loft Subdivision Surface_
|	__Osds__		|	_SDS Subdivision Surface object_
|	__Osweep__		|	_Sweep Subdivision Surface_

### Deformer Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
| 	__Obend__ 		|	_Bend Deformer_ 		
|	__Obulge__		|	_Bulge Deformer_	
|	__Oexplosion__		|	_Explosion deformer_		
|	__Oexplosionfx__	|	_Explosion FX object_	
|	__Offd__		|	_FFD_		
|	__Oformula__		|	_Formula deformer_	
|	__Omelt__		|	_Melt deformer_
|	__Oshatter__		|	_Shatter deformer_
|	__Oshear__		|	_Shear deformer_
|	__Opolyreduction__	|	_Polygon reduction object_
|	__Oskin__		|	_Skin deformer_
|	__Ospherify__		|	_Spherify object_
|	__Osplinedeformer__	|	_Spline deformer object_
|	__Osplinerail__		|	_Spline rail object_
|	__Otaper__		|	_Taper deformer_
|	__Otwist__		|	_Twist deformer_
|	__Owave__		|	_Wave deformer_
|	__Owinddeform__		|	_Wind deformer_
|	__Owrap__		|	_Wrap deformer_

### Environment Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
| 	__Obackground__ 	| 	_Background_ 	
|	__Oenvironment__	|	_Environment_	
|	__Ofloor__		|	_Floor_				
|	__Oforeground__		|	_Foreground_	
|	__Osky__		|	_Sky_
|	__Ostage__		|	_Stage_

### Particle Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
| 	__Oattractor__ 		|	_Particle Attractor_ 		
|	__Odeflector__		|	_Particle Deflector_		
|	__Odestructor__		|	_Particle Destructor_	
|	__Ofriction__		|	_Particle friction_		
|	__Ogravitation__	|	_Particle gravitation_		
|	__Oparticle__		|	_Particle emitter_
|	__Oparticlemodifier__	|	_Particle modifier_
|	__Orotation__		|	_Particle rotation_
|	__Oturbulence__		|	_Particle turbulence_
|	__Owind__		|	_Particle wind_

### Other Objects
|BaseObject Type (SDK name) 	| Common name in C4D GUI		|
|:------------------------------| :-----------------------------------: |
|	__Ocamera__		|	_Camera_				
|	__Ocharacter__		|	_Character Object_		
|	__Ocmotion__		|	_CMotion Object_		
|	__Oconnector__		|	_Connector Object_		
|	__Ofractal__		|	_Fractal object_		
|	__Oheadphone__		|	_Headphone_				
|	__Ojoint__		|	_Joint object_			
|	__Olight__		|	_Light_						
|	__Oloudspeaker__	|	_Loudspeaker_
|	__Omicrophone__		|	_Microphone_
|	__Oplugin__		|  	_Plugin object - pass the plugin ID_
|	__Opluginpolygon__	|	_Polygon plugin object_
|	__Oselection__		|	_Selection object_
|	__Oshowdisplacement__	|	_Show displacement_
|	__Oweighteffector__	|	_Weight effector_
|	__Oworkplane__		|	_Work plane_
|	__Oxref__		|	_XRef object_
|	__Omotiontracker__	|	_Motion tracker object_
