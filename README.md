# REO Survivors (Vampire Survivors-style) — OOP Final Team Project (PyGame)

## Team
- **Team Name**: Dsaiubu
- **Members**
  1) นาย ปรีชา แสงแก้ว — ออกแบบระบบ/ออกแบบเกมเพลย์/เขียนโค้ด
  2) นาย ภานุวัฒน์ ไชยเพชร — ลูกกระจ้อก

## Project Overview
มันคือเกมที่คุณต้องรับบทเป็น **ฮีโร่ตัวน้อย** สู้กับศัตรูที่โถมเข้ามาเป็นกองทัพนับพันใน **แผนที่กว้าง ๆ**

**Core Loop (เกมเพลย์หลัก)**
- ผู้เล่นทำแค่ **เดิน** (Move)
- ตัวละครจะ **โจมตีอัตโนมัติ** (Auto-Attack) ตามจังหวะเวลา
- เมื่อเก็บเม็ดค่าประสบการณ์ **EXP** จากศัตรูที่ตาย → **เลเวลอัพ** แล้วเลือก **อัปเกรดความสามารถ**

**เงื่อนไขชนะ (Win Condition)**
- อยู่รอดครบ **60 วินาที** (ปรับได้ที่ `GameConfig.win_time_seconds`) → ชนะ

## Why this genre fits an OOP/SOLID project
จุดเด่นที่ทำให้เกมแนวนี้เหมาะกับการทำโปรเจกต์ส่งอาจารย์ คือสามารถโชว์ OOP/SOLID ได้ “ชัด” และ “แยกส่วน” ได้ดี:

- **Class Hierarchy (Inheritance)**: สร้าง `Entity` เป็นคลาสแม่ แล้วให้ `Player` และ `Enemy` สืบทอด
- **Encapsulation**: เก็บค่า HP/ความเร็ว/สเตตัสไว้ในคลาส (เช่น `Health`, `Stats`) ไม่ให้โค้ดส่วนอื่นแก้ตรง ๆ
- **Composition**: แยกคลาส `Weapon` ออกจากตัวละคร แล้วให้ผู้เล่น “ถือ” อาวุธไว้ใน `Player.weapons`
- **Polymorphism**: อาวุธทุกชนิดมี interface เดียวกัน แต่ logic ต่างกัน (เช่น `MagicWand`, `Knife`) และเพิ่มอาวุธใหม่ได้โดยไม่ต้องแก้ `Player`

## Tech Stack
- **Python 3.11+**
- **PyGame Community Edition (`pygame-ce`)**

## How to Run
### 1) Create venv (optional but recommended)
```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

หรือแบบ `pyproject.toml`:
```bash
pip install -e .
```

### 3) Run
```bash
python -m reo_survivors
```

## Run with uv (optional)
ถ้าใช้ `uv`:
```bash
uv run -m reo_survivors
```

หรือ:
```bash
uv run main.py
```

หรือ (หลัง `uv pip install -e .` / `pip install -e .`):
```bash
reo-survivors
```

## Controls
- **WASD / Arrow Keys**: Move
- **ESC**: Pause / Resume
- **Enter**: Start (ในหน้าเมนู) / Confirm (ตอนเลือกอัปเกรด)
- **1 / 2 / 3**: เลือกอัปเกรดตอน Level Up

## OOP + SOLID + Design Patterns (What we demonstrate)
### OOP Concepts
- **Encapsulation**: `Health`, `Cooldown`, `EventBus` ซ่อน state และ expose method ที่จำเป็น
- **Inheritance**: `Entity` -> `Player`, `Enemy`, `Projectile`, `Gem`
- **Polymorphism**: `Weapon` หลายชนิด (`MagicWand`, `Knife`) ใช้งานผ่าน interface เดียวกัน
- **Composition**: `Player` ประกอบด้วย `Health`, `Weapon` หลายชิ้น, และ `Stats`

### SOLID Principles
- **S (Single Responsibility)**:
  - `EnemySpawner` ทำหน้าที่ spawn
  - `CollisionSystem` ทำหน้าที่ตรวจชน
  - `Upgrade` ทำหน้าที่ apply upgrade
- **O (Open/Closed)**:
  - เพิ่มอาวุธ/อัปเกรดใหม่ได้โดยสร้างคลาสใหม่ ไม่ต้องแก้แกนหลักมาก
- **L (Liskov Substitution)**:
  - ทุก `Weapon` ใช้งานแทนกันได้ใน `Player.weapons`
- **I (Interface Segregation)**:
  - แยกความสามารถเป็น interface/Protocol เล็ก ๆ (เช่น `Updatable`, `Drawable`)
- **D (Dependency Inversion)**:
  - `PlayState` รับ dependency เป็น object (เช่น spawner / event_bus) แทนการผูกกับ global

### Design Patterns
- **State Pattern**: `MenuState`, `PlayState`, `PauseState`, `GameOverState`
- **Strategy Pattern**: `Weapon` เป็น strategy ของการยิง/โจมตี
- **Factory Pattern**: `EnemyFactory` สร้างศัตรูตาม difficulty/time
- **Observer (Pub/Sub)**: `EventBus` กระจาย event เช่น `EnemyKilled`, `LeveledUp`

## Project Structure
```
OOP-project/
  pyproject.toml
  requirements.txt
  README.md
  src/
    reo_survivors/
      __init__.py
      __main__.py
      app.py
      config.py
      core/
        events.py
        math2d.py
        time.py
      entities/
        base.py
        player.py
        enemy.py
        projectile.py
        gem.py
      systems/
        collision.py
        spawner.py
        upgrades.py
      states/
        base.py
        menu.py
        play.py
        pause.py
        game_over.py
      weapons/
        base.py
        magic_wand.py
        knife.py
```