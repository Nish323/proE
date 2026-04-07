def predict(data):
    """
    簡単な動作確認用の関数
    """
    return f"モデルがデータ '{data}' を受け取りました。正常に動作しています！"

if __name__ == "__main__":
    # このファイルが直接実行された時だけ動くテストコード
    print("--- Model.py 起動テスト開始 ---")
    
    test_input = "テストデータ"
    result = predict(test_input)
    
    print(f"結果: {result}")
    print("--- Model.py 起動テスト完了 ---")