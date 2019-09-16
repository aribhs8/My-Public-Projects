# import files + pygame
import pygame
import random
from settings import *
from pow import *
from Explosion import *

# collision detection function
def collisionCheck(game):
    # timer
    now = pygame.time.get_ticks()

    # detect collisions among sprites
    # player collisions
    player_platformHits = pygame.sprite.spritecollide(game.player, game.platforms, False)
    player_wallHits = pygame.sprite.spritecollide(game.player, game.walls, False)
    player_roofHits = pygame.sprite.spritecollide(game.player, game.top, False)
    player_boxHits = pygame.sprite.spritecollide(game.player, game.boxes, False)
    player_meleeEnemyHits = pygame.sprite.spritecollide(game.player, game.meleeEnemies, False)
    player_shootEnemyHits = pygame.sprite.spritecollide(game.player, game.shooterEnemies, False)
    player_lightningHits = pygame.sprite.spritecollide(game.player, game.lightning, False)
    player_powerupHits = pygame.sprite.spritecollide(game.player, game.powerups, False)
    player_gunShotHits = pygame.sprite.spritecollide(game.player, game.gunShots, True)
    player_doorCollide = pygame.sprite.spritecollide(game.player, game.doors, False)

    # batarang collisions
    batarang_meleeHits = pygame.sprite.groupcollide(game.meleeEnemies, game.batarangs, False, True)
    batarang_gunHits = pygame.sprite.groupcollide(game.shooterEnemies, game.batarangs, False, True)
    explosion_meleeHits = pygame.sprite.groupcollide(game.meleeEnemies, game.explosions, False, False)
    explosion_shootHits = pygame.sprite.groupcollide(game.shooterEnemies, game.explosions, False, False)

    if game.level == 1:
        for door in game.doors:
            if player_doorCollide:
                door.open = True
            else:
                door.open = False

        # detect if player gets hit by bullet
        if player_gunShotHits:
            game.player.shield -= 5
            game.player.damage = True

        # detect if explosion hits surrounding enemies
        for enemy_hit in explosion_meleeHits:
            if now - game.updateLast > 200:
                game.updateLast = now
                enemy_hit.health -= 10

        for enemy_hit in explosion_shootHits:
            if now - game.updateLast > 200:
                game.updateLast = now
                enemy_hit.health -= 10

        # batarang vs meleeEnemies
        for batarangHit in batarang_meleeHits:
            game.updateLast = now
            if game.player.power == 1:
                batarangHit.health -= 5
            elif game.player.power == 2:
                batarangHit.health -= 20
                expl = Explosion(game, batarangHit.rect.center)
                game.explosionSound.play()
            game.comboCounter += 2
            batarangHit.attacked = True

        # batarang vs shootEnemies
        for batarangHit in batarang_gunHits:
            game.updateLast = now
            if game.player.power == 1:
                batarangHit.health -= 5
            elif game.player.power == 2:
                batarangHit.health -= 20
                expl = Explosion(game, batarangHit.rect.center)
                game.explosionSound.play()

            game.comboCounter += 2
            batarangHit.attacked = True

        if now - game.batarangStun > 1000 and not player_meleeEnemyHits and not player_shootEnemyHits and not explosion_meleeHits:
            for enemy in game.meleeEnemies:
                enemy.attacked = False
            for enemy in game.shooterEnemies:
                enemy.attacked = False
            game.batarangStun = now

        # player vs meleeEnemies
        for villain in player_meleeEnemyHits:
            if game.player.attacking:
                if game.player.rect.left < villain.rect.centerx and game.player.direction == "R" or game.player.rect.right > villain.rect.centerx and game.player.direction == "L" \
                    or game.player.rect.centerx == villain.rect.centerx or game.player.rect.left < villain.rect.centerx and game.player.direction == "R" or game.player.rect.centerx > villain.rect.right \
                    and game.player.direction == "L":
                    if now - game.updateLast > 200:
                        villain.health -= 10
                        game.comboCounter += 1
                        game.updateLast = now
                    villain.attacking = False
                    villain.attacked = True
                    if villain.rect.right > game.player.rect.left and villain.rect.left < game.player.rect.left:
                        villain.vel.x = -KNOCKBACK
                    elif villain.rect.left < game.player.rect.right and villain.rect.right > game.player.rect.right:
                        villain.vel.x = KNOCKBACK

            else:
                villain.attacking = True
                villain.attacked = False
           
                if now - game.updateLast > 500:
                    game.player.damage = True
                    game.comboCounter = 0
                    game.updateLast = now 
                    game.player.shield -= 10

        # player vs shooterEnemies
        for villain in player_shootEnemyHits:
            if game.player.attacking:
                if now - game.updateLast > 200:
                    villain.health -= 10
                    game.comboCounter += 1
                    game.score += game.comboCounter - (game.comboCounter * (game.totalTime / 10000000))
                    game.updateLast = now
                villain.attacking = False
                villain.attacked = True
                if villain.rect.right > game.player.rect.left and villain.rect.left < game.player.rect.left:
                    villain.vel.x = -KNOCKBACK
                elif villain.rect.left < game.player.rect.right and villain.rect.right > game.player.rect.right:
                    villain.vel.x = KNOCKBACK
            else:
                villain.attacking = True
                villain.attacked = False
                if now - game.updateLast > 600:
                    game.comboCounter = 0
                    game.player.damage = True
                    game.updateLast = now 
                    game.player.shield -= 10

        if not player_shootEnemyHits and not player_meleeEnemyHits and not player_gunShotHits:
            game.player.attack_frame = 0
            game.player.damage = False
            if now - game.updateLast > 500:
                game.comboCounter = 0
            for enemy in game.meleeEnemies:
                enemy.attacking = False
            for enemy in game.shooterEnemies:
                enemy.attacking = False

        # lightning hits
        for lightning_hits in player_lightningHits:
            game.player.damage = True
            if now - game.updateLast > 1000:
                game.updateLast = now
                game.player.shield -= 5

        # reset timer to 0
        if not player_shootEnemyHits and not player_lightningHits and not player_meleeEnemyHits and game.comboCounter == 0 and not explosion_meleeHits and not explosion_shootHits:
            game.updateLast = now


    # player platform hits
    for plat_hits in player_platformHits:
        # if player is falling
        if game.player.vel.y >= 0:
            # if player's top is higher than the platform's bottom and the player
            if game.player.rect.top < plat_hits.rect.bottom and game.player.rect.centery > plat_hits.rect.top + 1:
                # if player is moving left
                if game.player.vel.x < 0:
                    game.player.pos.x = plat_hits.rect.right + 25
                # if player is moving right 
                elif game.player.vel.x > 0:
                    game.player.pos.x = plat_hits.rect.left - 25
            else:
                game.player.vel.y = 0
                game.player.pos.y = plat_hits.rect.top + 1

        # if player is jumping
        elif game.player.vel.y < 0:
            if game.player.rect.top > plat_hits.rect.centery and game.player.rect.bottom > plat_hits.rect.bottom:
                game.player.vel.y = -PLAYER_JUMP
            else:
                # the player is moving left
                if game.player.vel.x < 0:
                    game.player.pos.x = plat_hits.rect.right + 25
                # if the player is moving right
                elif game.player.vel.x > 0:
                    game.player.pos.x = plat_hits.rect.left - 25

    # player wall hits
    for wall_hits in player_wallHits:
        # if player moving right
        if game.player.vel.x > 0:
            game.player.pos.x = wall_hits.rect.left - 25
        # if player moving left
        elif game.player.vel.x < 0:
            game.player.pos.x = wall_hits.rect.right + 25

    # player and power-ups
    for hit in player_powerupHits:
        game.updateLast = now
        if hit.type == "explosion":
            game.player.power = 2
            game.player.quantity += 5
            game.attackPowerUp_sound.play()
        if hit.type == "shield":
            game.player.shield += 25
            game.healSound.play()
        hit.kill()

    for roof_hit in player_roofHits:
        game.player.vel.y = GRAV

    # player box hits
    for box_hits in player_boxHits:
        # if the player's center y-value is more than the box's top
        if game.player.rect.centery < box_hits.rect.top:
            if game.player.pos.x < box_hits.rect.right + 10 and \
                game.player.pos.x > box_hits.rect.left - 10:
                game.player.vel.y = 0
                game.player.pos.y = box_hits.rect.top + 1
        # if the player's center y-value is less than the box's top
        elif game.player.rect.centery > box_hits.rect.top and game.player.rect.centery < box_hits.rect.bottom:
            # if the player is moving right
            if game.player.vel.x > 0:
                game.player.pos.x = box_hits.rect.left - 25
            # if the player is moving left
            elif game.player.vel.x < 0:
                game.player.pos.x = box_hits.rect.right + 25
        else:
            game.player.vel.y = -PLAYER_JUMP

    # LEVEL 2
    if game.level == 2:
        # boss
        boss_platformHits = pygame.sprite.spritecollide(game.boss, game.platforms, False)
        boss_playerHits = pygame.sprite.collide_rect(game.boss, game.player)
        boulder_playerHits = pygame.sprite.spritecollide(game.player, game.boulders, True)
        boulder_pillarHits = pygame.sprite.groupcollide(game.boulders, game.pillars, True, True)
        batarang_bossHits = pygame.sprite.spritecollide(game.boss, game.batarangs, True)

        # player
        player_pillarHits = pygame.sprite.spritecollide(game.player, game.pillars, False)


        for hit in boulder_pillarHits:
            if random.random() > 0.5:
                pow = Pow(game, "explosion", hit.rect.centerx, hit.rect.centery)

        if boulder_playerHits:
            game.player.shield -= 10
            game.player.damage = True

        # batarang vs boss
        for batarangHit in batarang_bossHits:
            game.updateLast = now
            if game.player.power == 2:
                game.boss.hitCount += 1
                if game.boss.hitCount >= 3:
                    game.boss.health -= 5
                    game.boss.throwing = False
                    game.boss.throwFrame = 0
                    game.boss.dazed = True
                    game.boss.hitCount = 0
                expl = Explosion(game, game.boss.rect.center)
                game.explosionSound.play()
                game.comboCounter += 2

        # player vs boss
        if boss_playerHits:
            if game.player.attacking and game.boss.dazed:
                if now - game.updateLast > 500:
                    game.updateLast = now
                    game.boss.health -= 2
                    game.comboCounter += 1
            else:
                if now - game.updateLast > 800:
                    game.player.damage = True
                    game.comboCounter = 0
                    game.updateLast = now 
                    game.player.shield -= 10
        else:
            game.comboCounter = 0
            game.player.damage = False
            game.updateLast = now

        # if boss is falling
        if game.boss.vel.y > 0:
            # if boss hits platform
            if boss_platformHits:
                game.boss.vel.y = 0
                game.boss.pos.y = boss_platformHits[0].rect.top + 1

        for pillar in player_pillarHits:
            # if player is falling
            if game.player.vel.y >= 0:
                # if player's top is higher than the platform's bottom and the player
                if game.player.rect.top < pillar.rect.bottom and game.player.rect.centery > pillar.rect.top + 1:
                    # if player is moving left
                    if game.player.vel.x < 0:
                        game.player.pos.x = pillar.rect.right + 25
                    # if player is moving right 
                    elif game.player.vel.x > 0:
                        game.player.pos.x = pillar.rect.left - 25

            # if player is jumping
            elif game.player.vel.y < 0:
                if game.player.rect.top > pillar.rect.centery and game.player.rect.bottom > pillar.rect.bottom:
                    game.player.vel.y = -PLAYER_JUMP
                else:
                    # the player is moving left
                    if game.player.vel.x < 0:
                        game.player.pos.x = pillar.rect.right + 25
                    # if the player is moving right
                    elif game.player.vel.x > 0:
                        game.player.pos.x = pillar.rect.left - 25
