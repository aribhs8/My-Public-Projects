package com.mygdx.game.Actors.Enemies;

import com.badlogic.gdx.graphics.g2d.Animation;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.physics.box2d.World;
import com.mygdx.game.Actors.SuperActors.Character;
import com.mygdx.game.Base.BaseGame;
import com.mygdx.game.Utilities.Constants;
import com.mygdx.game.Utilities.SpriteSheet;

public class DaggerEnemy extends Character {
    // FIELDS
    // control
    private float minRange;
    private float maxRange;
    public char direction;
    public TextureRegion logo;

    // game
    private BaseGame game;

    public DaggerEnemy(BaseGame g, float minRange, float maxRange) {
        super(Constants.DAGGER_ENEMY_DAMAGE);
        this.game = g;
        this.minRange = minRange;
        this.maxRange = maxRange;
        this.direction = 'F';
        this.loadAssets();
    }

    // SETUP METHODS
    @Override
    public void loadAssets() {
        // SpriteSheet
        SpriteSheet spriteSheet = new SpriteSheet("enemies/goblin_goon_dagger_sprite_sheet.png", this.game);

        // walk animation
        int[][] walkImage_coordinates = {{14, 67, 28, 53}, {76, 68, 28, 52}, {144, 67, 29, 52},
                {207, 67, 35, 52}, {267, 68, 46, 52}, {338, 67, 34, 53}};
        Animation<TextureRegion> walkAnim = spriteSheet.getAnimation
                (walkImage_coordinates, 0.15f, Animation.PlayMode.LOOP_PINGPONG);
        this.storeAnimation("walk", walkAnim);

        // attack animation
        int[][] attackImage_coordinates = {{404, 67, 29, 53}, {471, 67, 24, 53}, {535, 67, 47, 53},
                {602, 67, 40, 53}, {664, 67, 35, 53}};
        Animation<TextureRegion> attackAnim = spriteSheet.getAnimation
                (attackImage_coordinates, 0.10f, Animation.PlayMode.LOOP);
        this.storeAnimation("attack", attackAnim);

        // death animation
        int[][] deathImage_coordinates = {{83, 272, 29, 46}, {138, 283, 42, 35}};
        Animation<TextureRegion> deathAnim = spriteSheet.getAnimation
                (deathImage_coordinates, 0.25f, Animation.PlayMode.NORMAL);
        this.storeAnimation("death", deathAnim);

        // damage image
        TextureRegion damageReg = spriteSheet.getImage(83, 272, 29, 46);
        this.storeAnimation("damage", damageReg);

        logo = spriteSheet.getImage(83, 272, 29, 46);
    }

    @Override
    public void setProperties(World world) {
        this.setDynamic();
        this.setShapeRectangle();
        this.setPhysicsProperties(Constants.DAGGER_ENEMY_DENSITY, Constants.DAGGER_ENEMY_FRICTION,
                Constants.RESTITUTION);
        this.setMaxSpeed(Constants.DAGGER_ENEMY_MAX_WALK_SPEED);
        this.fixtureDef.filter.categoryBits = Constants.ENEMY_ENTITY;
        this.fixtureDef.filter.maskBits = Constants.WORLD_ENTITY|Constants.PLAYER_ENTITY|Constants.PLAYER_BULLET_ENTITY;
        this.setFixedRotation();
        this.initializePhysics(world);
    }

    // UPDATE METHODS
    @Override
    public void update() {
        this.move();
        this.animate();
    }
    private void move() {
        if (this.getX() >= this.maxRange && this.minRange != this.maxRange) this.direction = 'B';
        else if (this.getX() <= this.minRange && this.minRange != this.maxRange) this.direction = 'F';

        if (!this.getAnimationName().equals("damage")) {
            if (this.direction == 'F') {
                this.setScale(1, 1);
                this.applyForce(new Vector2(1f, 0));
            } else if (this.direction == 'B') {
                this.setScale(-1, 1);
                this.applyForce(new Vector2(-1f, 0));
            }
        }
    }
    private void animate() {
        if (this.getAnimationName().equals("walk")) {
            if (this.getTarget() != null) {
                if (!this.getTarget().getAnimationName().equals("punch") && !this.getTarget().getAnimationName().equals("upKick")
                        && !this.getTarget().getAnimationName().equals("uppercut")) {
                    this.setActiveAnimation("attack");
                } else {
                    this.setActiveAnimation("damage");
                }
            }
        }
        if (this.getAnimationName().equals("attack")) {
            if (this.getTarget() != null) {
                if (!this.getTarget().getAnimationName().equals("punch") && !this.getTarget().getAnimationName().equals("upKick")
                        && !this.getTarget().getAnimationName().equals("uppercut")) {
                    if (this.isAnimationFinished()) {

                        // set direction of target
                        if (this.getX() > this.getTarget().getX()) this.getTarget().setScaleX(1);
                        else this.getTarget().setScaleX(-1);

                        // change animations
                        if (this.getTarget().getHealth() > 0) this.getTarget().setActiveAnimation("damage");
                        if (this.getX() < this.getTarget().getX())
                            this.getTarget().applyImpulse(new Vector2(0.10f, 0.15f));
                        else this.getTarget().applyImpulse(new Vector2(-0.15f, 0.15f));

                        this.getTarget().setHealth(this.getDamage());
                        this.resetAnimation("attack");
                    }
                } else this.setActiveAnimation("damage");
            } else this.setActiveAnimation("walk");
        }
        if (this.getAnimationName().equals("damage")) {
            if (this.getTarget() != null) {
                if (!this.getTarget().getAnimationName().equals("punch") && !this.getTarget().getAnimationName().equals("upKick")
                        && !this.getTarget().getAnimationName().equals("uppercut")) {
                    this.setActiveAnimation("attack");
                }
                this.getBody().setLinearVelocity(0, 0);
            }
            else this.setActiveAnimation("walk");
        }
        if (this.getHealth() <= 0) {
            this.setActiveAnimation("death");
            this.getBody().setLinearVelocity(0, 0);
        }
    }
}
