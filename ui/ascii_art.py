def get_cafe_art(cafe_name, day):
    return f"""
    ☕ {cafe_name} ☕    
        )))
        (((
    +-----+
    |     |]
    `-----'    
    ___________
    `---------'
    День {day}
    """

def get_pet_art(pet_name):
    pets = {
        "Котик": r"""
        /_/\  
       ( o.o ) 
        > ^ <
        """,
        "Собачка": r"""
         ___
        /o o\ 
       (  ^  ) 
        | - |
        """,
        "Хомячок": r"""
         (__/)
         (o^-^o)
        """
    }
    return pets.get(pet_name, "Питомец не найден!")