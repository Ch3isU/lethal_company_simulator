class Monster:
    def __init__(self, name) -> None:
        self.name = name
    def death_message(self, playername):
        return f"{playername} was killed by {self.name}."
    
class Bracken(Monster):
    def __init__(self) -> None:
        super().__init__("Bracken")

    def death_message(self, playername):
        return f"{playername}`s neck was snapped by Bracken."
    
class Spider(Monster):
    def __init__(self) -> None:
        super().__init__("Spider")
    def death_message(self, playername):
        return f"{playername} stepped into a Spiders web and was killed."
    
class Thumper(Monster):
    def __init__(self) -> None:
        super().__init__("Thumper")
    def death_message(self, playername):
        return f"{playername} was hunted down by a Thumper."
    
class Snareflee(Monster):
    def __init__(self) -> None:
        super().__init__("Snareflee")
    def death_message(self, playername):
        return f"{playername} did not look at the ceiling and was killed by a Snareflee."
    
class EyelessDog(Monster):
    def __init__(self) -> None:
        super().__init__("Eyeless Dog")
    def death_message(self, playername):
        return f"{playername} could not keep quiet and was aten by an eyeless dog."
    
class FreddyFazbear(Monster):
    def __init__(self) -> None:
        super().__init__("Freddy Fazbear")
    def death_message(playername):
        return f"{playername} heared a quite ur ur ur ur ur and was killed by Freddy Fazbear."


class Monsters:
    BRACKEN = Bracken()
    SPIDER = Spider()
    THUMPER = Thumper()
    SNAREFLEE = Snareflee()
    EYELESS_DOG = EyelessDog()
    FREDDY = FreddyFazbear()
