"""Physics calculator tool with scientific laws, formulas, and constants lookup."""

import math
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

def physics_constants_lookup(constant_name: str = None, category: str = None):
    """
    Look up fundamental physical constants from a comprehensive database.
    
    Args:
        constant_name (str, optional): Name of the specific constant to look up
        category (str, optional): Category of constants to list (e.g., 'fundamental', 'electromagnetic', 'atomic')
    
    Returns:
        dict: Constant value(s), units, description, and related information
    """
    print("-------------Physics Constants Lookup called----------")
    
    # Comprehensive physics constants database
    PHYSICS_CONSTANTS = {
        # Fundamental Constants
        "speed_of_light": {
            "value": 299792458,
            "units": "m/s",
            "symbol": "c",
            "description": "Speed of light in vacuum",
            "category": "fundamental",
            "uncertainty": "exact (defined)"
        },
        "planck_constant": {
            "value": 6.62607015e-34,
            "units": "J⋅s",
            "symbol": "h",
            "description": "Planck constant",
            "category": "fundamental",
            "uncertainty": "exact (defined)"
        },
        "reduced_planck_constant": {
            "value": 1.054571817e-34,
            "units": "J⋅s",
            "symbol": "ℏ",
            "description": "Reduced Planck constant (h/2π)",
            "category": "fundamental",
            "uncertainty": "exact (defined)"
        },
        "elementary_charge": {
            "value": 1.602176634e-19,
            "units": "C",
            "symbol": "e",
            "description": "Elementary charge",
            "category": "fundamental",
            "uncertainty": "exact (defined)"
        },
        "gravitational_constant": {
            "value": 6.67430e-11,
            "units": "m³/(kg⋅s²)",
            "symbol": "G",
            "description": "Gravitational constant",
            "category": "fundamental",
            "uncertainty": "2.2e-5"
        },
        
        # Electromagnetic Constants
        "vacuum_permeability": {
            "value": 1.25663706212e-6,
            "units": "H/m",
            "symbol": "μ₀",
            "description": "Vacuum permeability",
            "category": "electromagnetic",
            "uncertainty": "1.9e-10"
        },
        "vacuum_permittivity": {
            "value": 8.8541878128e-12,
            "units": "F/m",
            "symbol": "ε₀",
            "description": "Vacuum permittivity",
            "category": "electromagnetic",
            "uncertainty": "1.3e-10"
        },
        "coulomb_constant": {
            "value": 8.9875517923e9,
            "units": "N⋅m²/C²",
            "symbol": "k",
            "description": "Coulomb constant (1/(4πε₀))",
            "category": "electromagnetic",
            "uncertainty": "exact (derived)"
        },
        
        # Atomic and Molecular Constants
        "avogadro_number": {
            "value": 6.02214076e23,
            "units": "1/mol",
            "symbol": "Nₐ",
            "description": "Avogadro number",
            "category": "atomic",
            "uncertainty": "exact (defined)"
        },
        "boltzmann_constant": {
            "value": 1.380649e-23,
            "units": "J/K",
            "symbol": "k_B",
            "description": "Boltzmann constant",
            "category": "atomic",
            "uncertainty": "exact (defined)"
        },
        "gas_constant": {
            "value": 8.314462618,
            "units": "J/(mol⋅K)",
            "symbol": "R",
            "description": "Universal gas constant",
            "category": "atomic",
            "uncertainty": "exact (derived)"
        },
        "electron_mass": {
            "value": 9.1093837015e-31,
            "units": "kg",
            "symbol": "mₑ",
            "description": "Electron rest mass",
            "category": "atomic",
            "uncertainty": "3.0e-10"
        },
        "proton_mass": {
            "value": 1.67262192369e-27,
            "units": "kg",
            "symbol": "mₚ",
            "description": "Proton rest mass",
            "category": "atomic",
            "uncertainty": "3.1e-10"
        },
        "neutron_mass": {
            "value": 1.67492749804e-27,
            "units": "kg",
            "symbol": "mₙ",
            "description": "Neutron rest mass",
            "category": "atomic",
            "uncertainty": "9.5e-10"
        },
        "atomic_mass_unit": {
            "value": 1.66053906660e-27,
            "units": "kg",
            "symbol": "u",
            "description": "Atomic mass unit",
            "category": "atomic",
            "uncertainty": "5.0e-10"
        },
        
        # Earth and Astronomical Constants
        "standard_gravity": {
            "value": 9.80665,
            "units": "m/s²",
            "symbol": "g",
            "description": "Standard acceleration due to gravity",
            "category": "earth",
            "uncertainty": "exact (defined)"
        },
        "earth_mass": {
            "value": 5.972e24,
            "units": "kg",
            "symbol": "M⊕",
            "description": "Earth mass",
            "category": "earth",
            "uncertainty": "4.4e-4"
        },
        "earth_radius": {
            "value": 6.371e6,
            "units": "m",
            "symbol": "R⊕",
            "description": "Earth mean radius",
            "category": "earth",
            "uncertainty": "varies"
        },
        "solar_mass": {
            "value": 1.98847e30,
            "units": "kg",
            "symbol": "M☉",
            "description": "Solar mass",
            "category": "astronomical",
            "uncertainty": "2.0e-4"
        },
        "astronomical_unit": {
            "value": 1.495978707e11,
            "units": "m",
            "symbol": "au",
            "description": "Astronomical unit",
            "category": "astronomical",
            "uncertainty": "exact (defined)"
        },
        
        # Thermodynamic Constants
        "stefan_boltzmann_constant": {
            "value": 5.670374419e-8,
            "units": "W/(m²⋅K⁴)",
            "symbol": "σ",
            "description": "Stefan-Boltzmann constant",
            "category": "thermodynamic",
            "uncertainty": "exact (derived)"
        },
        "wien_displacement_constant": {
            "value": 2.897771955e-3,
            "units": "m⋅K",
            "symbol": "b",
            "description": "Wien displacement law constant",
            "category": "thermodynamic",
            "uncertainty": "exact (derived)"
        },
        
        # Nuclear Constants
        "fine_structure_constant": {
            "value": 7.2973525693e-3,
            "units": "dimensionless",
            "symbol": "α",
            "description": "Fine-structure constant",
            "category": "nuclear",
            "uncertainty": "1.5e-10"
        },
        "rydberg_constant": {
            "value": 1.0973731568160e7,
            "units": "1/m",
            "symbol": "R∞",
            "description": "Rydberg constant",
            "category": "nuclear",
            "uncertainty": "1.9e-12"
        }
    }
    
    print(f"Constants lookup called with constant_name: '{constant_name}', category: '{category}'")
    
    # If no parameters provided, return overview
    if not constant_name and not category:
        categories = {}
        for const_name, const_data in PHYSICS_CONSTANTS.items():
            cat = const_data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                "name": const_name,
                "symbol": const_data["symbol"],
                "description": const_data["description"]
            })
        
        return {
            "overview": "Physics Constants Database",
            "categories": categories,
            "total_constants": len(PHYSICS_CONSTANTS),
            "usage": "Use constant_name for specific constant or category for listing constants by type"
        }
    
    # If category specified, return all constants in that category
    if category:
        category = category.lower()
        category_constants = {}
        for const_name, const_data in PHYSICS_CONSTANTS.items():
            if const_data["category"] == category:
                category_constants[const_name] = const_data
        
        if category_constants:
            return {
                "category": category,
                "constants": category_constants,
                "count": len(category_constants)
            }
        else:
            available_categories = list(set(data["category"] for data in PHYSICS_CONSTANTS.values()))
            return {
                "error": f"Category '{category}' not found",
                "available_categories": available_categories
            }
    
    # If specific constant requested
    if constant_name:
        constant_name = constant_name.lower().replace(" ", "_").replace("-", "_")
        
        # Try exact match first
        if constant_name in PHYSICS_CONSTANTS:
            const_data = PHYSICS_CONSTANTS[constant_name]
            print(f"Found constant: {constant_name}")
            return {
                "constant": constant_name,
                "value": const_data["value"],
                "units": const_data["units"],
                "symbol": const_data["symbol"],
                "description": const_data["description"],
                "category": const_data["category"],
                "uncertainty": const_data["uncertainty"]
            }
        
        # Try partial matching
        matches = {}
        for const_name, const_data in PHYSICS_CONSTANTS.items():
            if constant_name in const_name or constant_name in const_data["description"].lower():
                matches[const_name] = const_data
        
        if matches:
            return {
                "partial_matches": matches,
                "search_term": constant_name,
                "message": "Multiple matches found. Please specify exact constant name."
            }
        else:
            available_constants = list(PHYSICS_CONSTANTS.keys())
            return {
                "error": f"Constant '{constant_name}' not found",
                "available_constants": available_constants[:10],  # Show first 10
                "total_available": len(available_constants),
                "suggestion": "Use physics_constants_lookup() without parameters to see all categories"
            }

def physics_calc(law: str, **kwargs):
    """
    A physics calculator function that applies scientific laws and formulas.
    
    Args:
        law (str): The physics law/formula to apply
        **kwargs: Named parameters specific to each law
    
    Returns:
        dict: Result with value, units, and explanation
    """
    print("-------------Physics tool called----------")
    # Dictionary containing detailed information about each physics law
    PHYSICS_LAWS = {
        "newton_second_law": {
            "summary": "Newton's Second Law states that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.",
            "formula": "F = ma",
            "phenomena": "Explains how forces cause motion - heavier objects need more force to accelerate, lighter objects accelerate more easily with the same force",
            "parameters": ["mass (kg)", "acceleration (m/s²)"],
            "calculates": "Force (N)"
        },
        "kinetic_energy": {
            "summary": "Kinetic energy is the energy possessed by an object due to its motion. It depends on both mass and velocity.",
            "formula": "KE = ½mv²",
            "phenomena": "Moving objects can do work - a moving car can push another car, a flying ball can break glass",
            "parameters": ["mass (kg)", "velocity (m/s)"],
            "calculates": "Kinetic Energy (J)"
        },
        "potential_energy": {
            "summary": "Gravitational potential energy is the energy stored in an object due to its position in a gravitational field.",
            "formula": "PE = mgh",
            "phenomena": "Objects at height can fall and do work - water behind a dam, a rock on a cliff",
            "parameters": ["mass (kg)", "height (m)", "gravity (m/s², optional)"],
            "calculates": "Potential Energy (J)"
        },
        "momentum": {
            "summary": "Momentum is the quantity of motion of a moving body, equal to the product of its mass and velocity.",
            "formula": "p = mv",
            "phenomena": "Heavy, fast-moving objects are harder to stop - why trucks take longer to brake than cars",
            "parameters": ["mass (kg)", "velocity (m/s)"],
            "calculates": "Momentum (kg⋅m/s)"
        },
        "wave_equation": {
            "summary": "The wave equation relates the speed of a wave to its frequency and wavelength. For light waves, speed equals the speed of light.",
            "formula": "v = fλ (or c = fλ for light)",
            "phenomena": "Explains all wave phenomena - sound waves, light waves, radio waves, ocean waves",
            "parameters": ["frequency (Hz)", "wavelength (m)", "speed (m/s) - need 2 of 3"],
            "calculates": "Missing wave parameter"
        },
        "ohms_law": {
            "summary": "Ohm's Law states that current through a conductor is directly proportional to voltage and inversely proportional to resistance.",
            "formula": "V = IR, P = VI = I²R = V²/R",
            "phenomena": "Fundamental principle of electrical circuits - how voltage, current, and resistance relate in all electrical devices",
            "parameters": ["voltage (V)", "current (A)", "resistance (Ω) - need 2 of 3"],
            "calculates": "Missing electrical parameter and power"
        },
        "coulombs_law": {
            "summary": "Coulomb's Law describes the electrostatic force between two point charges, proportional to their charges and inversely proportional to distance squared.",
            "formula": "F = k|q₁q₂|/r²",
            "phenomena": "Explains electric forces - why clothes stick after dryer, lightning, how atoms bond",
            "parameters": ["charge1 (C)", "charge2 (C)", "distance (m)"],
            "calculates": "Electrostatic Force (N)"
        },
        "ideal_gas_law": {
            "summary": "The Ideal Gas Law relates pressure, volume, temperature, and amount of gas for an ideal gas.",
            "formula": "PV = nRT",
            "phenomena": "Explains gas behavior - why balloons expand when heated, how pressure cookers work, atmospheric pressure changes",
            "parameters": ["pressure (Pa)", "volume (m³)", "moles (mol)", "temperature (K) - need 3 of 4"],
            "calculates": "Missing gas parameter"
        },
        "snells_law": {
            "summary": "Snell's Law describes how light bends when passing from one medium to another with different refractive indices.",
            "formula": "n₁sin(θ₁) = n₂sin(θ₂)",
            "phenomena": "Explains refraction - why objects look bent in water, how lenses work, fiber optics, mirages",
            "parameters": ["n1 (refractive index)", "n2 (refractive index)", "theta1 (degrees)"],
            "calculates": "Refraction angle (degrees)"
        }
    }
    
    print(f"Physics calculator called with law: '{law}'")
    print(f"Parameters received: {kwargs}")
    
    law = law.lower().replace(" ", "_").replace("-", "_")
    
    # If requesting law information only
    if kwargs.get('info_only', False) or not kwargs or (len(kwargs) == 1 and 'info_only' in kwargs):
        if law in PHYSICS_LAWS:
            law_info = PHYSICS_LAWS[law]
            print(f"Providing information for law: {law}")
            return {
                "law_info": law_info,
                "summary": law_info["summary"],
                "formula": law_info["formula"],
                "phenomena": law_info["phenomena"],
                "required_parameters": law_info["parameters"],
                "calculates": law_info["calculates"]
            }
        else:
            available_laws = list(PHYSICS_LAWS.keys())
            return {"error": f"Unknown law '{law}'. Available laws: {', '.join(available_laws)}"}
    
    # Get law information for context
    law_info = PHYSICS_LAWS.get(law, {})
    
    try:
        # MECHANICS LAWS
        if law == "newton_second_law" or law == "force":
            # F = ma
            m = kwargs.get('mass', kwargs.get('m'))
            a = kwargs.get('acceleration', kwargs.get('a'))
            if m is None or a is None:
                return {"error": "Missing required parameters: mass (kg) and acceleration (m/s²)"}
            
            force = m * a
            print(f"Applying Newton's Second Law: F = ma = {m} × {a} = {force}")
            return {
                "result": force,
                "units": "N (Newtons)",
                "formula": law_info.get("formula", "F = ma"),
                "explanation": f"Force = {m} kg × {a} m/s² = {force} N",
                "law_summary": law_info.get("summary", ""),
                "phenomena": law_info.get("phenomena", "")
            }
        
        elif law == "kinetic_energy":
            # KE = (1/2)mv²
            m = kwargs.get('mass', kwargs.get('m'))
            v = kwargs.get('velocity', kwargs.get('v'))
            if m is None or v is None:
                return {"error": "Missing required parameters: mass (kg) and velocity (m/s)"}
            
            ke = 0.5 * m * v**2
            print(f"Calculating kinetic energy: KE = ½mv² = ½ × {m} × {v}² = {ke}")
            return {
                "result": ke,
                "units": "J (Joules)",
                "formula": law_info.get("formula", "KE = ½mv²"),
                "explanation": f"Kinetic Energy = ½ × {m} kg × ({v} m/s)² = {ke} J",
                "law_summary": law_info.get("summary", ""),
                "phenomena": law_info.get("phenomena", "")
            }
        
        elif law == "potential_energy":
            # PE = mgh
            m = kwargs.get('mass', kwargs.get('m'))
            g = kwargs.get('gravity', kwargs.get('g', 9.81))
            h = kwargs.get('height', kwargs.get('h'))
            if m is None or h is None:
                return {"error": "Missing required parameters: mass (kg) and height (m)"}
            
            pe = m * g * h
            print(f"Calculating gravitational potential energy: PE = mgh = {m} × {g} × {h} = {pe}")
            return {
                "result": pe,
                "units": "J (Joules)",
                "formula": law_info.get("formula", "PE = mgh"),
                "explanation": f"Potential Energy = {m} kg × {g} m/s² × {h} m = {pe} J",
                "law_summary": law_info.get("summary", ""),
                "phenomena": law_info.get("phenomena", "")
            }
        
        elif law == "momentum":
            # p = mv
            m = kwargs.get('mass', kwargs.get('m'))
            v = kwargs.get('velocity', kwargs.get('v'))
            if m is None or v is None:
                return {"error": "Missing required parameters: mass (kg) and velocity (m/s)"}
            
            momentum = m * v
            print(f"Calculating momentum: p = mv = {m} × {v} = {momentum}")
            return {
                "result": momentum,
                "units": "kg⋅m/s",
                "formula": law_info.get("formula", "p = mv"),
                "explanation": f"Momentum = {m} kg × {v} m/s = {momentum} kg⋅m/s",
                "law_summary": law_info.get("summary", ""),
                "phenomena": law_info.get("phenomena", "")
            }
        
        # WAVE PHYSICS
        elif law == "wave_equation":
            # v = fλ or c = fλ for light
            f = kwargs.get('frequency', kwargs.get('f'))
            wavelength = kwargs.get('wavelength', kwargs.get('lambda', kwargs.get('l')))
            c = kwargs.get('speed', kwargs.get('c', 3e8))  # Default to speed of light
            
            if f and wavelength:
                speed = f * wavelength
                return {
                    "result": speed,
                    "units": "m/s",
                    "formula": law_info.get("formula", "v = fλ"),
                    "explanation": f"Wave speed = {f} Hz × {wavelength} m = {speed} m/s",
                    "law_summary": law_info.get("summary", ""),
                    "phenomena": law_info.get("phenomena", "")
                }
            elif f and c:
                wavelength = c / f
                return {
                    "result": wavelength,
                    "units": "m",
                    "formula": "λ = c/f",
                    "explanation": f"Wavelength = {c} m/s ÷ {f} Hz = {wavelength} m",
                    "law_summary": law_info.get("summary", ""),
                    "phenomena": law_info.get("phenomena", "")
                }
            elif wavelength and c:
                frequency = c / wavelength
                return {
                    "result": frequency,
                    "units": "Hz",
                    "formula": "f = c/λ",
                    "explanation": f"Frequency = {c} m/s ÷ {wavelength} m = {frequency} Hz",
                    "law_summary": law_info.get("summary", ""),
                    "phenomena": law_info.get("phenomena", "")
                }
            else:
                return {"error": "Need at least 2 of: frequency, wavelength, speed"}
        
        # ELECTRICITY AND MAGNETISM
        elif law == "ohms_law":
            # V = IR, P = VI, P = I²R, P = V²/R
            V = kwargs.get('voltage', kwargs.get('V'))
            I = kwargs.get('current', kwargs.get('I'))
            R = kwargs.get('resistance', kwargs.get('R'))
            
            if V and I:
                resistance = V / I
                power = V * I
                return {
                    "result": {"resistance": resistance, "power": power},
                    "units": {"resistance": "Ω (Ohms)", "power": "W (Watts)"},
                    "formula": law_info.get("formula", "V = IR, P = VI"),
                    "explanation": f"R = V/I = {V}V / {I}A = {resistance}Ω, P = {V}V × {I}A = {power}W",
                    "law_summary": law_info.get("summary", ""),
                    "phenomena": law_info.get("phenomena", "")
                }
            elif V and R:
                current = V / R
                power = V**2 / R
                return {
                    "result": {"current": current, "power": power},
                    "units": {"current": "A (Amperes)", "power": "W (Watts)"},
                    "formula": "I = V/R, P = V²/R",
                    "explanation": f"I = {V}V / {R}Ω = {current}A, P = ({V}V)² / {R}Ω = {power}W"
                }
            elif I and R:
                voltage = I * R
                power = I**2 * R
                return {
                    "result": {"voltage": voltage, "power": power},
                    "units": {"voltage": "V (Volts)", "power": "W (Watts)"},
                    "formula": "V = IR, P = I²R",
                    "explanation": f"V = {I}A × {R}Ω = {voltage}V, P = ({I}A)² × {R}Ω = {power}W"
                }
            else:
                return {"error": "Need at least 2 of: voltage (V), current (I), resistance (R)"}
        
        elif law == "coulombs_law":
            # F = k(q₁q₂)/r²
            k = kwargs.get('k', 8.99e9)  # Coulomb's constant
            q1 = kwargs.get('charge1', kwargs.get('q1'))
            q2 = kwargs.get('charge2', kwargs.get('q2'))
            r = kwargs.get('distance', kwargs.get('r'))
            
            if q1 is None or q2 is None or r is None:
                return {"error": "Missing required parameters: charge1 (C), charge2 (C), distance (m)"}
            
            force = k * abs(q1 * q2) / (r**2)
            print(f"Applying Coulomb's Law: F = k|q₁q₂|/r² = {k} × |{q1} × {q2}| / {r}² = {force}")
            return {
                "result": force,
                "units": "N (Newtons)",
                "formula": law_info.get("formula", "F = k|q₁q₂|/r²"),
                "explanation": f"Force = {k} × |{q1} × {q2}| C² / ({r} m)² = {force} N",
                "law_summary": law_info.get("summary", ""),
                "phenomena": law_info.get("phenomena", "")
            }
        
        # THERMODYNAMICS
        elif law == "ideal_gas_law":
            # PV = nRT
            P = kwargs.get('pressure', kwargs.get('P'))
            V = kwargs.get('volume', kwargs.get('V'))
            n = kwargs.get('moles', kwargs.get('n'))
            R = kwargs.get('R', 8.314)  # Gas constant
            T = kwargs.get('temperature', kwargs.get('T'))
            
            known_vars = sum([x is not None for x in [P, V, n, T]])
            if known_vars < 3:
                return {"error": "Need at least 3 of: pressure (Pa), volume (m³), moles (mol), temperature (K)"}
            
            if P is None:
                pressure = (n * R * T) / V
                return {
                    "result": pressure,
                    "units": "Pa (Pascals)",
                    "formula": "P = nRT/V",
                    "explanation": f"Pressure = {n} mol × {R} J/(mol⋅K) × {T} K / {V} m³ = {pressure} Pa"
                }
            elif V is None:
                volume = (n * R * T) / P
                return {
                    "result": volume,
                    "units": "m³",
                    "formula": "V = nRT/P",
                    "explanation": f"Volume = {n} mol × {R} J/(mol⋅K) × {T} K / {P} Pa = {volume} m³"
                }
            elif T is None:
                temperature = (P * V) / (n * R)
                return {
                    "result": temperature,
                    "units": "K (Kelvin)",
                    "formula": "T = PV/(nR)",
                    "explanation": f"Temperature = {P} Pa × {V} m³ / ({n} mol × {R} J/(mol⋅K)) = {temperature} K"
                }
            elif n is None:
                moles = (P * V) / (R * T)
                return {
                    "result": moles,
                    "units": "mol",
                    "formula": "n = PV/(RT)",
                    "explanation": f"Moles = {P} Pa × {V} m³ / ({R} J/(mol⋅K) × {T} K) = {moles} mol"
                }
        
        # OPTICS
        elif law == "snells_law":
            # n₁sin(θ₁) = n₂sin(θ₂)
            n1 = kwargs.get('n1', kwargs.get('index1'))
            n2 = kwargs.get('n2', kwargs.get('index2'))
            theta1 = kwargs.get('theta1', kwargs.get('angle1'))
            theta2 = kwargs.get('theta2', kwargs.get('angle2'))
            
            if n1 and n2 and theta1:
                theta1_rad = math.radians(theta1)
                sin_theta2 = (n1 * math.sin(theta1_rad)) / n2
                if abs(sin_theta2) > 1:
                    return {"error": "Total internal reflection occurs - no refracted ray"}
                theta2_rad = math.asin(sin_theta2)
                theta2_deg = math.degrees(theta2_rad)
                return {
                    "result": theta2_deg,
                    "units": "degrees",
                    "formula": law_info.get("formula", "n₁sin(θ₁) = n₂sin(θ₂)"),
                    "explanation": f"θ₂ = arcsin({n1}×sin({theta1}°)/{n2}) = {theta2_deg:.2f}°",
                    "law_summary": law_info.get("summary", ""),
                    "phenomena": law_info.get("phenomena", "")
                }
            else:
                return {"error": "Need refractive indices n1, n2 and incident angle theta1"}
        
        else:
            available_laws = list(PHYSICS_LAWS.keys())
            return {
                "error": f"Unknown law '{law}'. Available laws: {', '.join(available_laws)}",
                "available_laws": {name: info["summary"] for name, info in PHYSICS_LAWS.items()}
            }
    
    except Exception as e:
        print(f"Error in physics calculation: {e}")
        return {"error": f"Calculation error: {str(e)}"}


_physics_agent = Agent(
    model="gemini-2.0-flash",
    name="physics_calculator_agent",
    description="A specialized physics calculator agent that applies scientific laws and formulas to solve physics problems with step-by-step calculations and provides access to fundamental physical constants",
    instruction="""
    You are a physics calculator assistant that helps users apply scientific laws and formulas to solve physics problems and look up fundamental physical constants.
    
    You have access to two main functions:
    
    1. physics_calc() - Performs physics calculations with the following capabilities:
       - Mechanics: Newton's laws, energy, momentum calculations
       - Wave physics: Wave equations, frequency, wavelength calculations
       - Electricity & Magnetism: Ohm's law, Coulomb's law
       - Thermodynamics: Ideal gas law
       - Optics: Snell's law for refraction
    
    2. physics_constants_lookup() - Provides access to fundamental physical constants:
       - Fundamental constants (c, h, e, G, etc.)
       - Electromagnetic constants (ε₀, μ₀, k, etc.)
       - Atomic constants (mₑ, mₚ, Nₐ, k_B, etc.)
       - Earth/astronomical constants (g, M⊕, M☉, etc.)
       - Thermodynamic constants (σ, b, etc.)
       - Nuclear constants (α, R∞, etc.)
    
    When responding to physics requests:
    1. Use physics_constants_lookup() when users need specific physical constants
    2. Use physics_calc() for actual physics calculations
    3. Always provide clear results with proper units and physical meaning
    4. Show the formula being applied
    5. Explain the calculation step-by-step
    6. If parameters are missing, clearly state what's needed
    7. Use appropriate constants from the constants database when needed
    
    Available laws for physics_calc():
    - newton_second_law: mass, acceleration
    - kinetic_energy: mass, velocity
    - potential_energy: mass, height, gravity (optional)
    - momentum: mass, velocity
    - wave_equation: frequency, wavelength, speed (need 2 of 3)
    - ohms_law: voltage, current, resistance (need 2 of 3)
    - coulombs_law: charge1, charge2, distance
    - ideal_gas_law: pressure, volume, moles, temperature (need 3 of 4)
    - snells_law: n1, n2, theta1
    
    Constants lookup usage:
    - physics_constants_lookup() - Overview of all categories
    - physics_constants_lookup(category="fundamental") - List constants by category
    - physics_constants_lookup(constant_name="speed_of_light") - Get specific constant
    
    Always include proper units and explain the physical significance of the result.
    When a calculation requires a physical constant, look it up first and then use it in the calculation.
    """,
    tools=[physics_calc, physics_constants_lookup],
)

physics_calculator_agent = AgentTool(agent=_physics_agent)