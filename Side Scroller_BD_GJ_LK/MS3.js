class MainScene extends Phaser.Scene 
{
    constructor() 
    {
        super("MainScene")
        this.playerHealth = 1;
        this.plySpd = 400;
        this.playerScore = null;
        this.worldLevel = null;
        this.player = null;
        this.joystick = null;
        this.controlsEnabled = false;
        this.jumping = false;
        this.ground = null;
        this.Distance = Phaser.Math.Distance;
        this.gameOver = false;

        this.signals = SignalManager.get();
        this.walkSpeed = 300;
        this.jumpSpeed = 425;

        this.enemies = [];
        this.enemyImg = null;
        this.enemyPlayerCollider = null;

        // Camera object
        this.spriteCamera = null;
        
        // Tilemap variables
        this.map = null;
        this.tileset = null;
        this.layers = {
            background: null,
            foreground: null,
            overhead: null
        }

        // Firebase stuff
        this.database = firebase.firestore();
        this.scoreTable = this.database.collection('HHSH');

    }

    init(data) 
    {
        // Get the username from the title screen
        this.username = data.username;
        if (this.username == "") 
        {
            // No username was provided
            this.username = "N/A";
        }
    }


    /**
    * Saves the player's score to the firestore database
    */
    async saveScore() 
    {
        let result = await this.scoreTable.add
            (
                {
                    name: this.username,
                    score: this.score
                }
            );

        if (result) console.log("Score saved successfully!");
        else console.log("Score failed to save!");
    }



    preload() 
    {
        this.load.audio('music', './assets/Minute Waltz.mp3');
        this.load.audio('exp', './assets/explosion_3.wav');
        this.load.spritesheet('player', './assets/spr_RoninIdle_strip.png',
            {
                frameWidth: 64,
                frameHeight: 64
            });

        this.load.spritesheet('bag of bones', './assets/Idle.png',
            {
                frameWidth: 150,
                frameHeight: 150
            });

        this.load.spritesheet('explosion', './assets/Explosion.png', 
        {
            frameWidth: 32,
            frameHeight: 32
        });

        this.load.image('background', './assets/0.png');
        //Load the tilemap assets
        this.load.image('Tiles', './assets/Tileset.png');
        this.load.tilemapTiledJSON('Map', './assets/Platform-map.json');
        
        // Level two stuff
        //this.load.image('Tiles', './assets/Level_2_set.png');
        //this.load.tilemapTiledJSON('Map', './assets/Level_2.json');
    }


    create() 
    {
        // Background music
        let backgroundMusic = this.sound.add('music', { volume: 0.1 });

        backgroundMusic.play(
            {
                loop: true
            });


        // Background imagery
        let bg_Space = this.add.image(400, 400, 'background');
        bg_Space.setScale(6);


        // // Ground and gravity stuff
        // this.ground = this.add.rectangle(400, 250, 600, 30, 0xffffff, 1);   // Garrett Added this
        // this.ground = this.physics.add.existing(this.ground);
        // this.ground.body.setImmovable(true).setAllowGravity(false);


        //Add the Tilemap
        this.createMap();


        // Creating player and enemy and adding physics to them
        this.createPlayer();
        this.createEnemy();
        this.layers.foreground.setCollisionBetween(0,10000,true);
        this.physics.add.collider(this.player, this.layers.foreground);
        this.physics.add.collider(this.enemyImg, this.layers.foreground);

        // Start the controls overlay
        this.scene.launch("ControlScene");
        this.signals.on('joystick', (data) => 
        {
            this.movePlayer(data);
        });

        // Creating the joystick object
        // this.joystick = new VirtualJoystick(this, 70, 390, 45);
        this.controlsEnabled = true;

        // Create a button to jump on mobile
        // let jumpButton = this.add.circle(700, 390, 45, 0xFF0000, 0.4);
        // jumpButton.setInteractive();


        // When the player hits the button
        // jumpButton.on('pointerdown', () => {
        //     this.signals.emit('jump');
        // });

        this.signals.on('jump', () => {
            if (this.player.body.blocked.down) 
            {
                this.player.setVelocityY(-this.jumpSpeed);
            }
        });

        // Should allow jumping
        this.input.keyboard.on('keydown-SPACE', () => 
        {
            this.signals.emit('jump');
        });

        this.signals.on('jump', () => 
        {
            if (this.player.body.blocked.down) 
            {
                this.player.setVelocityY(-this.jumpSpeed);
            }
        });
        this.input.keyboard.on('keyup-SPACE', () => 
        {
            this.jumping = false;
        });


        // If the player stops clicking
        // jumpButton.on('pointerup', () =>  {
        //     this.jumping = false;
        // });
        // jumpButton.on('pointerout', () => {
        //     this.jumping = false;
        // });


        this.createCamera();
    }


    createCamera() 
    {
        //Add a camera to the scene that focus on the player within a certain area
        this.spriteCamera = this.cameras.main.setBounds(0,0,10000,10000);
        this.spriteCamera.setZoom(1.5);
        this.spriteCamera.startFollow(this.player);
    }

    update() 
    {
        this.setCollidePlayerEnemy();

        // The Limit Y of the game.
        if(this.player.y > 2000)
        {
            //Maybe a different Scene.
            this.scene.restart();

        }

        // The Limit X of the game
    }

    onGameOver()
    {
        this.gameOver = false;
        this.scene.start('MainScene');
    }


    //Create the Tilemap
    createMap() 
    {
        this.map = this.add.tilemap('Map');

        //Create a variable that store the tileset images
        //this.tileset = this.map.addTilesetImage('Level_2_set', 'Tiles');
        this.tileset = this.map.addTilesetImage('Platform-set', 'Tiles');

        //Add the background(layer the player and entities walk infront of)
        this.backgroundLayer = this.map.createLayer('background', this.tileset, 0, 0);
        this.backgroundLayer.setDepth(2);

        //Add the foreground(layer which the player and entities walk on)
        this.foregroundLayer = this.map.createLayer('foreground', this.tileset, 0, 0);
        this.foregroundLayer.setDepth(1);

        //Add the overhead(layer which the player and entities walk behind)
        this.overheadLayer = this.map.createLayer('overhead', this.tileset, 0, 0);
        this.overheadLayer.setDepth(0);

        //Put the layers in an object so that they can accessed from different functions
        this.layers = 
        {
            background: this.backgroundLayer,
            foreground: this.foregroundLayer,
            overhead: this.overheadLayer
        };

    }

    
    createPlayer() 
    {
        this.player = this.physics.add.sprite(55, 100, 'player');
        this.player.setScale(1.25);

        // this.player.setGravity(0, 300);
        this.player.setSize(35, 40);
        this.player.body.setAllowGravity(true);
        this.player.body.setDamping(true);
        this.player.setDrag(0.9, 0.95);

        // Create aniamtions for the player
        this.generatePlayerAnimations();

        // Collide the player with world bounds
        // this.player.setCollideWorldBounds(true);

        // Start the player in idle
        this.player.anims.play('idle');
    }


    // Controls to move the player.
    movePlayer(joystick)
    {
        // if (this.player.body.blocked.down) 
        // {
        // this.player.setVelocityX(this.walkSpeed * joystick.joyX());
        // }

        if (joystick.joyX() < 0) 
        {
            this.player.setVelocityX(this.walkSpeed * joystick.joyX());    
            this.player.flipX = true;
        }

        else if (joystick.joyX()  > 0) 
        {
            this.player.flipX = false;
            this.player.setVelocityX(this.walkSpeed * joystick.joyX());
        }

        else
        {
            this.player.setVelocityX(0);
        }
    }

    generatePlayerAnimations() 
    {
        // Create the idle animation
        this.player.anims.create(
            {
                key: 'idle',
                frames: this.anims.generateFrameNumbers('player',
                    {
                        start: 0, end: 7
                    }),
                frameRate: 8,
                repeat: -1
            });

        // Create left / right animations
        this.player.anims.create(
            {
                key: 'left',
                frames: this.anims.generateFrameNumbers('player',
                    {
                        frames: [0, 3]
                    }),
                frameRate: 12
            });

        this.player.anims.create(
            {
                key: 'right',
                frames: this.anims.generateFrameNumbers('player',
                    {
                        frames: [4, 7]
                    }),
                frameRate: 12
            });

        // Explosion animation
        this.player.anims.create(
            {
                key: 'boom',
                frames: this.anims.generateFrameNumbers('explosion',
                    {
                        start: 0,
                        end: 7
                    }),
                frameRate: 8
            })
    }



    createEnemy() 
    {
        this.enemyImg = this.physics.add.sprite(500, 50, 'bag of bones');
        this.enemyImg.setScale(1.25);
        this.enemyImg.setOrigin(0.5);
        this.enemyImg.body.setGravityY(300);
        this.enemyImg.setSize(45, 50);
        this.enemyImg.flipX = true

        this.enemies.push(this.enemyImg);

        this.enemyImg.anims.create(
            {
                key: 'idle',
                frames: this.anims.generateFrameNumbers('bag of bones',
                    {
                        start: 0,
                        end: 3
                    }),
                frameRate: 8,
                repeat: -1
            });


        this.enemyImg.anims.create(
            {
                key: 'boom',
                frames: this.anims.generateFrameNumbers('explosion',
                    {
                        start: 0,
                        end: 7
                    }),
                frameRate: 8
            });

        
        this.enemyImg.on('animationcomplete-boom', () => 
        {
            // this.destroyEnemy();
            this.enemyImg.destroy();
            
        });

        this.enemyImg.setCollideWorldBounds(true);

        this.enemyImg.anims.play('idle');
    }

    setCollidePlayerEnemy() 
    {
        // Destroy any existing collision handler
        if (this.enemyPlayerCollider != null) 
        {
            this.enemyPlayerCollider.destroy();
        }

        // Create a new collision handler
        this.enemyPlayerCollider =
            this.physics.add.overlap(this.enemies, this.player,
                (en, ply) => 
                {
                    // Blow up the player
                    this.sound.play('exp', 
                    {
                        volume: 0.1
                    });

                    this.enemyImg.anims.play('boom');

                    // Set the enemy velocity to "float" down
                    en.setVelocity(0, this.plySpd / 2);


                    // Remove the enemy from the list of enemies
                    // this.enemies = this.enemies.filter((e) => {
                    //     return e !== en;
                    // });
                }
            );
    }

    
    destroyEnemy()
    {
        this.enemies = this.enemies.filter((e) => 
        {
            return e !== this.enemyImg;
        });

        this.enemyImg.body.destroy();
    }


    destroyPlayer() 
    {
        // Prevent multiple collision by removing player physics
        // body

        this.player.body.destroy();
        // Disable the player from further controlling the ship
        this.controlsEnabled = false;

        this.gameOver = true;
    }
}