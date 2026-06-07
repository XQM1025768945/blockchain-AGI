# 仿生脉冲编解码：8 字节头 + 64 维特征向量（极低带宽）

HEADER_SIZE = 8
VECTOR_SIZE = 64


def encode_spike(node_id: str, feature_vector: list) -> bytes:
    """将节点 ID 和特征向量编码为低带宽脉冲数据包。

    Args:
        node_id: 节点标识（取前 8 字节作为头部）
        feature_vector: 64 维特征向量（值域 0-255）

    Returns:
        bytes: 序列化后的二进制脉冲数据
    """
    header = node_id[:HEADER_SIZE].encode().ljust(HEADER_SIZE, b"\x00")
    if len(feature_vector) < VECTOR_SIZE:
        feature_vector = feature_vector + [0] * (VECTOR_SIZE - len(feature_vector))
    data = bytes(feature_vector[:VECTOR_SIZE])
    return header + data


def decode_spike(data: bytes) -> dict:
    """将二进制脉冲数据包解析回结构化对象。"""
    header = data[:HEADER_SIZE].decode(errors="ignore").strip("\x00").strip()
    vector = list(data[HEADER_SIZE : HEADER_SIZE + VECTOR_SIZE])
    return {"node": header, "vector": vector}


if __name__ == "__main__":
    sample = [int(i * 4) for i in range(VECTOR_SIZE)]
    packet = encode_spike("demo-node", sample)
    print("packet size (bytes):", len(packet))
    print("decoded:", decode_spike(packet))
