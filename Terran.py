import sc2
from sc2 import run_game, maps,Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import SUPPLYDEPOT,SCV, COMMANDCENTER


class BezzaBot(sc2.BotAI):

    async def on_step(self, iteration):
        await self.build_workers()
        await self.distribute_workers()
        await self.build_supplyDepot()

    async def build_workers(self):
        for center in self.units(COMMANDCENTER).ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < 16 * self.units(COMMANDCENTER).amount:
                await self.do(center.train(SCV))

    async def build_supplyDepot(self):
        if self.supply_left < 2 and not self.already_pending(SUPPLYDEPOT):
            centers = self.units(COMMANDCENTER).ready
            if centers.exists:
                if self.can_afford(SUPPLYDEPOT):
                    await self.build(SUPPLYDEPOT, near=centers.first)


run_game(maps.get("(2)AcidPlantLE"), [
    Bot(Race.Terran, BezzaBot()),
    Computer(Race.Zerg, Difficulty.Easy)
    ],realtime = True)