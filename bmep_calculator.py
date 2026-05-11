#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平均有効圧力（BMEP）計算プログラム
シリンダー数、1シリンダーあたりの容積、最大トルクと発生回転数から
平均有効圧力を計算します。
ロータリーエンジンにも対応しています。
"""

def calculate_bmep(num_cylinders, displacement_per_cylinder, max_torque, rpm, cycle_type, engine_type="reciprocating"):
    """
    平均有効圧力を計算する関数
    
    Parameters:
    -----------
    num_cylinders : int
        シリンダー数（往復動エンジン）またはロータ数（ロータリーエンジン）
    displacement_per_cylinder : float
        1シリンダーあたりの容積 (cc)（往復動エンジン）
        またはロータ当たりの容積 (cc)（ロータリーエンジン）
    max_torque : float
        最大トルク (N·m)
    rpm : int
        トルク発生回転数 (rpm)
    cycle_type : int
        エンジンサイクル (2 = 2サイクル, 4 = 4サイクル)
    engine_type : str
        エンジン形式 ("reciprocating" = 往復動, "rotary" = ロータリー)
    
    Returns:
    --------
    dict : 計算結果を含む辞書
    """
    
    # 総排気量を計算 (cc)
    total_displacement = num_cylinders * displacement_per_cylinder
    
    # 総排気量をリットルに変換
    total_displacement_liters = total_displacement / 1000
    
    # エンジン形式に応じた係数計算
    if engine_type == "reciprocating":
        engine_type_name = "往復動エンジン"
        
        if cycle_type == 2:
            cycle_factor = 1
            cycle_name = "2サイクル"
        elif cycle_type == 4:
            cycle_factor = 2
            cycle_name = "4サイクル"
        else:
            raise ValueError("サイクル数は2または4を指定してください")
    
    elif engine_type == "rotary":
        engine_type_name = "ロータリーエンジン"
        # ロータリーエンジンはローター1回転で2回のパワーストローク
        # 実質的には4サイクル相当の動作
        cycle_factor = 1  # ロータリーでは計算が異なる
        if cycle_type == 4:
            cycle_name = "4サイクル相当"
        else:
            cycle_name = f"{cycle_type}サイクル"
    
    else:
        raise ValueError('engine_type は "reciprocating" または "rotary" を指定してください')
    
    # BMEP計算（bar単位）
    if engine_type == "reciprocating":
        # 往復動エンジン: BMEP (bar) = (120 × トルク[N·m]) / (排気量[cc] × サイクル係数)
        bmep = (120 * max_torque * rpm) / (total_displacement * cycle_factor)
    else:
        # ロータリーエンジン: ローター1回転で2回のパワーストローク
        # BMEP (bar) = (60 × トルク[N·m] × rpm) / 排気量[cc]
        bmep = (60 * max_torque * rpm) / total_displacement
    
    # 結果を辞書で返す
    return {
        "num_cylinders": num_cylinders,
        "displacement_per_cylinder": displacement_per_cylinder,
        "total_displacement": total_displacement,
        "total_displacement_liters": total_displacement_liters,
        "max_torque": max_torque,
        "rpm": rpm,
        "engine_type": engine_type_name,
        "cycle_type": cycle_name,
        "bmep": bmep
    }


def display_result(result):
    """計算結果を見やすく表示する"""
    print("\n" + "="*60)
    print("平均有効圧力（BMEP）計算結果")
    print("="*60)
    print(f"エンジン形式: {result['engine_type']}")
    print(f"シリンダー/ロータ数: {result['num_cylinders']}")
    print(f"1シリンダー/ロータあたりの容積: {result['displacement_per_cylinder']} cc")
    print(f"総排気量: {result['total_displacement']} cc ({result['total_displacement_liters']:.2f} L)")
    print(f"最大トルク: {result['max_torque']} N·m")
    print(f"トルク発生回転数: {result['rpm']} rpm")
    print(f"エンジンサイクル: {result['cycle_type']}")
    print("-"*60)
    print(f"平均有効圧力（BMEP）: {result['bmep']:.2f} bar")
    print("="*60 + "\n")


def main():
    """メイン処理"""
    print("\n平均有効圧力（BMEP）計算プログラム")
    print("-"*60)
    
    try:
        # エンジン形式選択
        while True:
            engine_choice = input("エンジン形式を選択してください (1 = 往復動, 2 = ロータリー): ")
            if engine_choice == '1':
                engine_type = "reciprocating"
                break
            elif engine_choice == '2':
                engine_type = "rotary"
                break
            else:
                print("1 または 2 を入力してください。")
        
        # ユーザー入力
        if engine_type == "reciprocating":
            num_cylinders = int(input("シリンダー数を入力してください: "))
        else:
            num_cylinders = int(input("ロータ数を入力してください: "))
        
        if engine_type == "reciprocating":
            displacement_per_cylinder = float(input("1シリンダーあたりの容積 (cc) を入力してください: "))
        else:
            displacement_per_cylinder = float(input("1ロータあたりの容積 (cc) を入力してください: "))
        
        max_torque = float(input("最大トルク (N·m) を入力してください: "))
        rpm = int(input("トルク発生回転数 (rpm) を入力してください: "))
        
        # サイクル選択
        if engine_type == "reciprocating":
            while True:
                cycle_input = input("エンジンサイクルを選択してください (2 = 2サイクル, 4 = 4サイクル): ")
                if cycle_input in ['2', '4']:
                    cycle_type = int(cycle_input)
                    break
                else:
                    print("2 または 4 を入力してください。")
        else:
            # ロータリーエンジンは4サイクル相当固定
            cycle_type = 4
        
        # 計算実行
        result = calculate_bmep(num_cylinders, displacement_per_cylinder, max_torque, rpm, cycle_type, engine_type)
        
        # 結果表示
        display_result(result)
        
    except ValueError as e:
        print(f"\nエラー: 入力値が不正です。{e}")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
