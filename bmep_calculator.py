#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平均有効圧力（BMEP）計算プログラム
シリンダー数、1シリンダーあたりの容積、最大トルクと発生回転数から
平均有効圧力を計算します。
"""

def calculate_bmep(num_cylinders, displacement_per_cylinder, max_torque, rpm, cycle_type):
    """
    平均有効圧力を計算する関数
    
    Parameters:
    -----------
    num_cylinders : int
        シリンダー数
    displacement_per_cylinder : float
        1シリンダーあたりの容積 (cc)
    max_torque : float
        最大トルク (N·m)
    rpm : int
        トルク発生回転数 (rpm)
    cycle_type : int
        エンジンサイクル (2 = 2サイクル, 4 = 4サイクル)
    
    Returns:
    --------
    dict : 計算結果を含む辞書
    """
    
    # 総排気量を計算 (cc)
    total_displacement = num_cylinders * displacement_per_cylinder
    
    # 総排気量をリットルに変換
    total_displacement_liters = total_displacement / 1000
    
    # 平均有効圧力の計算式
    # BMEP (bar) = (2 × トルク[N·m] × 回転数[rpm]) / (排気量[cc] × サイクル数)
    # またはcc単位では
    # BMEP (bar) = (120 × トルク[N·m] × 回転数[rpm]) / (排気量[cc] × サイクル数)
    
    if cycle_type == 2:
        cycle_factor = 1
        cycle_name = "2サイクル"
    elif cycle_type == 4:
        cycle_factor = 2
        cycle_name = "4サイクル"
    else:
        raise ValueError("サイクル数は2または4を指定してください")
    
    # BMEP計算（bar単位）
    bmep = (120 * max_torque * rpm) / (total_displacement * cycle_factor)
    
    # 結果を辞書で返す
    return {
        "num_cylinders": num_cylinders,
        "displacement_per_cylinder": displacement_per_cylinder,
        "total_displacement": total_displacement,
        "total_displacement_liters": total_displacement_liters,
        "max_torque": max_torque,
        "rpm": rpm,
        "cycle_type": cycle_name,
        "bmep": bmep
    }


def display_result(result):
    """計算結果を見やすく表示する"""
    print("\n" + "="*60)
    print("平均有効圧力（BMEP）計算結果")
    print("="*60)
    print(f"シリンダー数: {result['num_cylinders']}")
    print(f"1シリンダーあたりの容積: {result['displacement_per_cylinder']} cc")
    print(f"総排気量: {result['total_displacement']} cc ({result['total_displacement_liters']:.2f} L)")
    print(f"最大トルク: {result['max_torque']} N·m")
    print(f"トルク発生回転数: {result['rpm']} rpm")
    print(f"エンジン形式: {result['cycle_type']}")
    print("-"*60)
    print(f"平均有効圧力（BMEP）: {result['bmep']:.2f} bar")
    print("="*60 + "\n")


def main():
    """メイン処理"""
    print("\n平均有効圧力（BMEP）計算プログラム")
    print("-"*60)
    
    try:
        # ユーザー入力
        num_cylinders = int(input("シリンダー数を入力してください: "))
        displacement_per_cylinder = float(input("1シリンダーあたりの容積 (cc) を入力してください: "))
        max_torque = float(input("最大トルク (N·m) を入力してください: "))
        rpm = int(input("トルク発生回転数 (rpm) を入力してください: "))
        
        while True:
            cycle_input = input("エンジンサイクルを選択してください (2 = 2サイクル, 4 = 4サイクル): ")
            if cycle_input in ['2', '4']:
                cycle_type = int(cycle_input)
                break
            else:
                print("2 または 4 を入力してください。")
        
        # 計算実行
        result = calculate_bmep(num_cylinders, displacement_per_cylinder, max_torque, rpm, cycle_type)
        
        # 結果表示
        display_result(result)
        
    except ValueError as e:
        print(f"\nエラー: 入力値が不正です。{e}")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
