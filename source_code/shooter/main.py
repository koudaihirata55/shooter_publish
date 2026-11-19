import pyxel
import math
import random

W,H = 160,120#画面の幅、高さ
player_speed=1.5
bullet_speed=2
enemy_w,enemy_h=12,12
sound_list={
    "bang":(0,0),
    "boom":(0,1),
    "hit":(0,2),
}
class base_sprite:
    def __init__(self,x,y,w=8,h=8,life=1):
        """コンストラクタ"""
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.life=life#HP
        self.vx,self.vy=0,0
    def update(self):
        """更新処理"""
    def draw(self):
        """描画(派生クラスで実装)"""

class player_sprite(base_sprite):
    def __init__(self, x, y,bullet,bomb,life):
        """コンストラクタ"""
        super().__init__(x, y,8,8,life)#親クラスのコンストラクタ(座標二つ,幅と高さ)
        self.cost="up"
        self.bullets=bullet
        self.bullet_frame_count=0
        self.bomb=bomb
        #コスチューム用意
        self.cost_list={
            "normal":(0,24,0,self.w,self.h,11),#イメージバンク番号,x,y,幅,高さ,透明扱いの色(ないなら空白)
            #"smile":(0,0,8,self.w,self.h),
            "right":(0,32,0,self.w,self.h,11),
            "left":(0,24,8,self.w,self.h,11),
            "up":(0,24,0,self.w,self.h,11),
            "down":(0,24,0,self.w,self.h,11),
            "damage":(0,32,8,self.w,self.h,11)
        }
    def update(self):
        """更新処理"""
        self.move_control()
        self.other_control()
        self.x+=self.vx;self.y+=self.vy
    def draw(self):
        """描画処理"""
        pyxel.blt(self.x,self.y,*self.cost_list[self.cost])
    def move(self, spd, deg):#放置で。
        """ 移動 """#角度
        rad = deg * math.pi / 180
        self.vx = spd * math.cos(rad) # x方向の速度
        self.vy = spd * math.sin(rad) # y方向の速度
    def move_control(self):
        if ( (pyxel.btn(pyxel.KEY_A) and not(pyxel.btn(pyxel.KEY_D) ) ) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) ) and 0<self.x+(self.w/2):
            if not self.cost=="damage":self.cost="left"
            self.vx=-1*player_speed
        elif ( pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) ) and (self.x+self.w)-(self.w/2) < W:
            if not self.cost=="damage":self.cost="right"
            self.vx=player_speed
        else:
            if not self.cost=="damage":self.cost="normal"
            self.vx=0
        
        if ( pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) ) and 0<self.y+(self.h/2):
            if not(self.cost=="right" or self.cost=="left" or self.cost=="damage"):self.cost="up"
            self.vy=-1*player_speed
        elif ( pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) ) and (self.y+self.h)-(self.w/2) < H:
            if not(self.cost=="right" or self.cost=="left" or self.cost=="damage"):self.cost="down"
            self.vy=player_speed
        else:
            self.vy=0
        
        if not(
            pyxel.btn(pyxel.KEY_A)or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) 
            ) and not(
                pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
            ) and not(
                pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) 
            ) and not(
                pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) ):#ニュートラル
            pass
            #self.cost="normal"
    def other_control(self):
        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B))and (pyxel.frame_count-self.bullet_frame_count>6):#スペースキーと前回の発射から6フレ
            self.bullets.append(bullet_sprite(self.x,self.y,2,6,cost=self.cost,speed=bullet_speed,bomb=self.bomb))
            self.bullet_frame_count=pyxel.frame_count
        if pyxel.btn(pyxel.KEY_SPACE):
            pass
            #self.cost="smile"

class enemy(base_sprite):
    def __init__(self, x, y,life):
        """コンストラクタ"""
        super().__init__(x, y,enemy_w,enemy_h,life)#親クラスのコンストラクタ(座標二つ,幅と高さ)
        self.vx=random.uniform(-2,2)
        self.vy=random.uniform(-2,2)
        self.cost="normal"
        self.n_frame=pyxel.frame_count
        self.a_frame=self.n_frame#左右の周期用フレームカウンター
        #コスチューム用意
        self.cost_list={
        "normal":(0,40,0,enemy_w,enemy_h,11)
            }
    def update(self):
        """更新処理"""
        self.move_control()
        self.x+=self.vx;self.y+=self.vy
    def draw(self):
        """描画処理"""
        pyxel.blt(self.x,self.y,*self.cost_list[self.cost])
    def move_control(self):
        self.n_frame=pyxel.frame_count
        if self.n_frame > self.a_frame+30:
            self.vx=random.uniform(-2,2)
            self.vy=random.uniform(-2,2)
            if 0>self.x+self.vx:self.vx=2#左に行きすぎたら強制的に右へ
            elif self.x+self.vx > W:self.vx=-2
            if 0 > self.y+self.vy:self.vy=2
            elif self.y+self.vy > H:self.vy=-2

            self.a_frame = self.n_frame

class bullet_sprite(base_sprite):
    def __init__(self, x, y,w=2,h=6,cost="normal",speed=1,bomb=[]):
        super().__init__(x, y,w,h)
        self.angle=cost
        self.speed=speed;self.w=w;self.h=h
        self.x=x+3;self.y=y
        self.bomb=bomb
        #角度によって生成場所変更
        #if self.angle == "up"or self.angle=="down": self.x=x+3;self.y=y
        #else: self.x=x;self.y=y+3
        pyxel.play(*sound_list["bang"])
    def update(self):
        """更新処理"""
        self.move()
        self.life_flag()
    def draw(self):
        """描画処理"""
        pyxel.rect(self.x,self.y,self.w,self.h,9)
        #属性によって玉の向きを変える
        #if self.angle=="up"or self.angle=="down":pyxel.rect(self.x,self.y,self.w,self.h,9)
        #else:pyxel.rect(self.x,self.y,self.w,self.h,9)
    def move(self):
        self.y-=self.speed
        #属性によって進む向きを変える
        #if self.angle=="up":self.y-=speed
        #elif self.angle=="down":self.y+=speed
        #elif self.angle=="right":self.x+=speed
        #elif self.angle=="left":self.x-=speed
    def life_flag(self):
       #画面内かどうか判定
       if not( (0<self.x+self.w<W) and (0<self.y<H) ):
           self.life=0
       #elif (enemy.x < self.x < enemy.x+7) and (enemy.y < self.y < enemy.y+8):
        #   self.life=0;self.bomb.append(bomb_particle(self.x,self.y,4))
       #else : self.life=1 
    
class snow_particle(base_sprite):#スノーパーティクル
    def __init__(self, x, y):
        super().__init__(x, y,1,1)
        self.vy=random.randint(2,8)/10
    def update(self):
        self.x+=self.vx;self.y+=self.vy
        if self.y > H:self.y=0
    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, 7)

class bomb_particle(base_sprite):#爆発パーティクル
    def __init__(self, x, y, size,col=10):
        super().__init__(x, y, size,size)
        pyxel.play(*sound_list["boom"])
        self.l_size=size#最終サイズ
        self.n_size=0#現在サイズ
        self.col=col#色指定
    def draw(self):
        """描画処理"""
        pyxel.circ(self.x,self.y,self.n_size,self.col)
    def update(self):
        """更新処理"""
        if self.l_size <= self.n_size : self.life=0
        else:self.n_size+=1
    
class Game:
    def __init__(self):
        """コンストラクタ"""
        #pyxel起動
        pyxel.init(W,H,title="shooter")#リセット
        #width(幅),height(高さ),title(タイトルバーの名前),fps(フレームレート),quit_key(閉じるキー指定),display_scale(表示倍率),capture_scale(録画の画質),capture_sec(録画最大秒数)
        pyxel.load("shooter_resource.pyxres")#ソースファイル読み込み
        self.bullets=[]#弾リスト
        self.bomb=[]#爆発パーティクルリスト
        self.enemy_list=[
            enemy(random.randint(0,W),H/4,1)for _ in range(10)
        ]#敵リスト
        self.snow_list = [#スノーパーティクルを50個生成
        snow_particle(random.randint(0, W), random.randint(0, H)) for _ in range(50)
        ]
        self.pose=0#0:スタート 1:プレイ 2:リザルト
        self.hit_frame=pyxel.frame_count
        self.score=0
        pyxel.run(self.update,self.draw)#実行関数(デフォルト毎秒30回)
    def update(self):
        """更新処理"""
        self.jadge_life()
        for s in self.snow_list: s.update()#スノーパーティクルのアップデート処理
        for b in self.bullets: b.update()#弾の更新処理
        for b in self.bomb:b.update()#爆発パーティクル更新処理
        for e in self.enemy_list: e.update()#敵更新処理

        if self.pose==0:
            # スペースキーが押されたらプレイヤーを生成してプレイ状態(1)へ
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START) :
                self.player_create()
                self.pose = 1
        elif self.pose == 1:
            self.jadge_hit()
            #プレイヤーのアップデートと爆殺処理
            if self.player.life<=0:
                self.bomb.extend([bomb_particle(self.player.x,self.player.y,20,8)])
                self.player.life+=-1
                self.pose=2
            elif self.player.life > 0: 
                self.player.update()
            else: 
                pass
        elif self.pose==2:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START) :self.pose = 0
    def draw(self):
        """描画処理"""
        pyxel.cls(0)#clear screen(画面の内容を消す)
        for s in self.snow_list: s.draw()##スノーパーティクルの描画処理
        for b in self.bullets: b.draw()#弾の描画処理
        for b in self.bomb: b.draw()#爆発パーティクルの描画処理
        for e in self.enemy_list : e.draw()#敵の描画処理

        if self.pose == 0 :
            pyxel.text(W/2-22,H/2,"PRESS START",14)
            #pyxel.text(W/2,H/2+10,"©koudai",14)
        elif self.pose==1 :
            self.player.draw()
            pyxel.text(10,10,f"HP:{self.player.life}",14)#playerとHP描画
            pyxel.text(10,20,f"SCORE:{self.score}",14)
        elif self.pose==2:
                pyxel.text((W/2)-18,(H/2)-3,"GAME OVER",14)
                pyxel.text((W/2)-2*len(f"SCORE:{self.score}"),(W/2)-8,f"SCORE:{self.score}",14)
    def jadge_hit(self):
        """当たり判定"""
        for e in self.enemy_list: 
            #敵と弾の当たり判定
            for b in self.bullets:
                if (e.x <= b.x+1 and b.x < e.x+enemy_w) and (e.y < b.y < e.y+enemy_h):
                    b.life += -1
                    e.life += -1
                    self.score+=1
                    if e.life > 0:pyxel.play(*sound_list["hit"])
            #敵とplayerの当たり判定
            if self.player.life > 0:
                if self.hit_frame+15 < pyxel.frame_count and (e.x+3 < self.player.x < e.x+8 or e.x+3 < self.player.x+7 < e.x+8) and (e.y < self.player.y < e.y+10 or e.y < self.player.y+7 < e.y+10):
                    self.player.life+= -1
                    pyxel.play(*sound_list["hit"],)
                    self.hit_frame=pyxel.frame_count
                elif self.hit_frame+15 > pyxel.frame_count:
                    self.player.cost="damage"
                else:
                    self.player.cost="normal"
    def jadge_life(self):
        """生存判定"""
        self.bullets[:] = [b for b in self.bullets if b.life > 0]#bulletsの中身を全部一つずつ取り出してlifeが1のインスタンスを抽出して入れ直す
        self.bomb.extend([bomb_particle(e.x,e.y,6) for e in self.enemy_list if e.life == 0]) #敵のHPがゼロになった時爆発パーティクル追加
        self.enemy_list.extend([enemy(random.randint(0,W),H/4,1) for e in self.enemy_list if e.life ==0])#上に同じく新しい敵生成
        self.bomb[:] = [b for b in self.bomb if b.life > 0]#爆発パーティクル生存判定
        self.enemy_list[:] = [e for e in self.enemy_list if e.life > 0]#敵生存判定
    def player_create(self):
        self.player=player_sprite(W/2,100,bullet=self.bullets,bomb=self.bomb,life=3)#プレイヤー生成
        self.score=0
        self.hit_frame=pyxel.frame_count


def main():
    """メイン処理"""
    Game()

if __name__ == "__main__":
    main()
        