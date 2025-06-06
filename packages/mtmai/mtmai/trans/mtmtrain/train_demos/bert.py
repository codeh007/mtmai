# 使用 pytorch 从零开始构建 bert 模型， 不过由于数据量太小看不出明显的预测结果，
# 教程： https://neptune.ai/blog/how-to-code-bert-using-pytorch-tutorial
# notebook: https://colab.research.google.com/drive/13FjI_uXaw8JJGjzjVX3qKSLyW9p3b6OV?usp=sharing

import logging
import math
import re
from random import *  # noqa: F403

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

logger = logging.getLogger()

# 训练数据集
text = (
    "Hello, how are you? I am Romeo.\n"
    "Hello, Romeo My name is Juliet. Nice to meet you.\n"
    "Nice meet you too. How are you today?\n"
    "Great. My baseball team won the competition.\n"
    "Oh Congratulations, Juliet\n"
    "Thanks you Romeo"
)


# 获取注意力的填充掩码
def get_attn_pad_mask(seq_q, seq_k):
    batch_size, len_q = seq_q.size()
    batch_size, len_k = seq_k.size()
    # # 等于零是PAD标记
    pad_attn_mask = seq_k.data.eq(0).unsqueeze(
        1
    )  # batch_size x 1 x len_k(=len_q), one is masking
    return pad_attn_mask.expand(batch_size, len_q, len_k)  # batch_size x len_q x len_k


# GELU 激活函数
def gelu(x):
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))


def train():
    # 处理文本数据
    sentences = re.sub("[.,!?\\-]", "", text.lower()).split(
        "\n"
    )  # filter '.', ',', '?', '!'
    word_list = list(set(" ".join(sentences).split()))
    word_dict = {"[PAD]": 0, "[CLS]": 1, "[SEP]": 2, "[MASK]": 3}

    for i, w in enumerate(word_list):
        word_dict[w] = i + 4
    number_dict = {i: w for i, w in enumerate(word_dict)}
    vocab_size = len(word_dict)

    token_list = list()
    for sentence in sentences:
        arr = [word_dict[s] for s in sentence.split()]
        token_list.append(arr)

    logger.info("show token list")
    print(token_list)

    maxlen = 30  # 序列最大长度
    batch_size = 6
    max_pred = 5  # 最大预测的token数量
    n_layers = 6  # 编码器层数
    n_heads = 12  # 多头注意力头数
    d_model = 768  # 嵌入维度
    d_ff = 768 * 4  # FeedForward维度
    d_k = d_v = 64  # K和V的维度
    n_segments = 2

    def make_batch():
        batch = []
        positive = negative = 0
        while positive != batch_size / 2 or negative != batch_size / 2:
            tokens_a_index, tokens_b_index = (
                randrange(len(sentences)),
                randrange(len(sentences)),
            )
            tokens_a, tokens_b = token_list[tokens_a_index], token_list[tokens_b_index]

            input_ids = (
                [word_dict["[CLS]"]]
                + tokens_a
                + [word_dict["[SEP]"]]
                + tokens_b
                + [word_dict["[SEP]"]]
            )

            segment_ids = [0] * (1 + len(tokens_a) + 1) + [1] * (len(tokens_b) + 1)

            # MASK LM
            n_pred = min(
                max_pred, max(1, int(round(len(input_ids) * 0.15)))
            )  # 15 % of tokens in one sentence(# 15% 的token需要进行预测)

            cand_maked_pos = [
                i
                for i, token in enumerate(input_ids)
                if token != word_dict["[CLS]"] and token != word_dict["[SEP]"]
            ]
            shuffle(cand_maked_pos)
            masked_tokens, masked_pos = [], []
            for pos in cand_maked_pos[:n_pred]:
                masked_pos.append(pos)
                masked_tokens.append(input_ids[pos])
                if random() < 0.8:  # 80%
                    input_ids[pos] = word_dict["[MASK]"]  # make mask
                elif random() < 0.5:  # 10%
                    index = randint(0, vocab_size - 1)  # random index in vocabulary
                    input_ids[pos] = word_dict[number_dict[index]]  # replace

            # Zero Paddings
            n_pad = maxlen - len(input_ids)
            input_ids.extend([0] * n_pad)
            segment_ids.extend([0] * n_pad)

            #     # Zero Padding (100% - 15%) tokens
            if max_pred > n_pred:
                n_pad = max_pred - n_pred
                masked_tokens.extend([0] * n_pad)
                masked_pos.extend([0] * n_pad)

            if tokens_a_index + 1 == tokens_b_index and positive < batch_size / 2:
                batch.append(
                    [input_ids, segment_ids, masked_tokens, masked_pos, True]
                )  # IsNext
                positive += 1
            elif tokens_a_index + 1 != tokens_b_index and negative < batch_size / 2:
                batch.append(
                    [input_ids, segment_ids, masked_tokens, masked_pos, False]
                )  # NotNext
                negative += 1
        return batch

    batch = make_batch()
    input_ids, segment_ids, masked_tokens, masked_pos, isNext = map(
        torch.LongTensor, zip(*batch, strict=False)
    )
    get_attn_pad_mask(input_ids, input_ids)[0][0], input_ids[0]

    # 多头注意力机制
    class MultiHeadAttention(nn.Module):
        def __init__(self):
            super(MultiHeadAttention, self).__init__()
            self.W_Q = nn.Linear(d_model, d_k * n_heads)
            self.W_K = nn.Linear(d_model, d_k * n_heads)
            self.W_V = nn.Linear(d_model, d_v * n_heads)

        def forward(self, Q, K, V, attn_mask):
            # q: [batch_size x len_q x d_model], k: [batch_size x len_k x d_model], v: [batch_size x len_k x d_model]
            residual, batch_size = Q, Q.size(0)
            # (B, S, D) -proj-> (B, S, D) -split-> (B, S, H, W) -trans-> (B, H, S, W)
            q_s = (
                self.W_Q(Q).view(batch_size, -1, n_heads, d_k).transpose(1, 2)
            )  # q_s: [batch_size x n_heads x len_q x d_k]
            k_s = (
                self.W_K(K).view(batch_size, -1, n_heads, d_k).transpose(1, 2)
            )  # k_s: [batch_size x n_heads x len_k x d_k]
            v_s = (
                self.W_V(V).view(batch_size, -1, n_heads, d_v).transpose(1, 2)
            )  # v_s: [batch_size x n_heads x len_k x d_v]

            attn_mask = attn_mask.unsqueeze(1).repeat(
                1, n_heads, 1, 1
            )  # attn_mask : [batch_size x n_heads x len_q x len_k]

            # context: [batch_size x n_heads x len_q x d_v], attn: [batch_size x n_heads x len_q(=len_k) x len_k(=len_q)]
            context, attn = ScaledDotProductAttention()(q_s, k_s, v_s, attn_mask)
            context = (
                context.transpose(1, 2).contiguous().view(batch_size, -1, n_heads * d_v)
            )  # context: [batch_size x len_q x n_heads * d_v]
            output = nn.Linear(n_heads * d_v, d_model)(context)
            return nn.LayerNorm(d_model)(
                output + residual
            ), attn  # output: [batch_size x len_q x d_model]

    # 嵌入层
    class Embedding(nn.Module):
        def __init__(self):
            super(Embedding, self).__init__()
            self.tok_embed = nn.Embedding(vocab_size, d_model)  # token 嵌入
            self.pos_embed = nn.Embedding(maxlen, d_model)  # 位置嵌入
            self.seg_embed = nn.Embedding(
                n_segments, d_model
            )  # segment(token type) embedding
            self.norm = nn.LayerNorm(d_model)

        def forward(self, x, seg):
            seq_len = x.size(1)
            pos = torch.arange(seq_len, dtype=torch.long)
            pos = pos.unsqueeze(0).expand_as(x)  # (seq_len,) -> (batch_size, seq_len)
            embedding = self.tok_embed(x) + self.pos_embed(pos) + self.seg_embed(seg)
            return self.norm(embedding)

    emb = Embedding()
    embeds = emb(input_ids, segment_ids)

    attenM = get_attn_pad_mask(input_ids, input_ids)

    class ScaledDotProductAttention(nn.Module):
        def __init__(self):
            super(ScaledDotProductAttention, self).__init__()

        def forward(self, Q, K, V, attn_mask):
            scores = torch.matmul(Q, K.transpose(-1, -2)) / np.sqrt(
                d_k
            )  # scores : [batch_size x n_heads x len_q(=len_k) x len_k(=len_q)]
            scores.masked_fill_(
                attn_mask, -1e9
            )  # Fills elements of self tensor with value where mask is one.
            attn = nn.Softmax(dim=-1)(scores)
            context = torch.matmul(attn, V)
            return context, attn

    SDPA = ScaledDotProductAttention()(embeds, embeds, embeds, attenM)

    # S, C, A = SDPA
    S, A = SDPA

    # print("Masks", masks[0][0])
    print()
    print("Scores: ", S[0][0], "\n\nAttention M: ", A[0][0])

    emb = Embedding()
    embeds = emb(input_ids, segment_ids)

    attenM = get_attn_pad_mask(input_ids, input_ids)

    MHA = MultiHeadAttention()(embeds, embeds, embeds, attenM)

    Output, A = MHA

    A[0][0]

    class PoswiseFeedForwardNet(nn.Module):
        def __init__(self):
            super(PoswiseFeedForwardNet, self).__init__()
            self.fc1 = nn.Linear(d_model, d_ff)
            self.fc2 = nn.Linear(d_ff, d_model)

        def forward(self, x):
            # (batch_size, len_seq, d_model) -> (batch_size, len_seq, d_ff) -> (batch_size, len_seq, d_model)
            return self.fc2(gelu(self.fc1(x)))

    # 编码器
    class EncoderLayer(nn.Module):
        def __init__(self):
            super(EncoderLayer, self).__init__()
            self.enc_self_attn = MultiHeadAttention()
            self.pos_ffn = PoswiseFeedForwardNet()

        def forward(self, enc_inputs, enc_self_attn_mask):
            enc_outputs, attn = self.enc_self_attn(
                enc_inputs, enc_inputs, enc_inputs, enc_self_attn_mask
            )  # enc_inputs to same Q,K,V
            enc_outputs = self.pos_ffn(
                enc_outputs
            )  # enc_outputs: [batch_size x len_q x d_model]
            return enc_outputs, attn

    class BERT(nn.Module):
        def __init__(self):
            super(BERT, self).__init__()
            self.embedding = Embedding()
            self.layers = nn.ModuleList([EncoderLayer() for _ in range(n_layers)])
            self.fc = nn.Linear(d_model, d_model)
            self.activ1 = nn.Tanh()
            self.linear = nn.Linear(d_model, d_model)
            self.activ2 = gelu
            self.norm = nn.LayerNorm(d_model)
            self.classifier = nn.Linear(d_model, 2)
            # decoder is shared with embedding layer
            embed_weight = self.embedding.tok_embed.weight
            n_vocab, n_dim = embed_weight.size()
            self.decoder = nn.Linear(n_dim, n_vocab, bias=False)
            self.decoder.weight = embed_weight
            self.decoder_bias = nn.Parameter(torch.zeros(n_vocab))

        def forward(self, input_ids, segment_ids, masked_pos):
            output = self.embedding(input_ids, segment_ids)
            enc_self_attn_mask = get_attn_pad_mask(input_ids, input_ids)
            for layer in self.layers:
                output, enc_self_attn = layer(output, enc_self_attn_mask)
            # output : [batch_size, len, d_model], attn : [batch_size, n_heads, d_mode, d_model]
            # it will be decided by first token(CLS)
            h_pooled = self.activ1(self.fc(output[:, 0]))  # [batch_size, d_model]
            logits_clsf = self.classifier(h_pooled)  # [batch_size, 2]

            masked_pos = masked_pos[:, :, None].expand(
                -1, -1, output.size(-1)
            )  # [batch_size, max_pred, d_model]
            # get masked position from final output of transformer.
            h_masked = torch.gather(
                output, 1, masked_pos
            )  # masking position [batch_size, max_pred, d_model]
            h_masked = self.norm(self.activ2(self.linear(h_masked)))
            logits_lm = (
                self.decoder(h_masked) + self.decoder_bias
            )  # [batch_size, max_pred, n_vocab]

            return logits_lm, logits_clsf

    logger.info("开始训练 bert 模型")
    model = BERT()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    batch = make_batch()
    input_ids, segment_ids, masked_tokens, masked_pos, isNext = map(
        torch.LongTensor, zip(*batch, strict=False)
    )

    for epoch in range(10):
        optimizer.zero_grad()
        logits_lm, logits_clsf = model(input_ids, segment_ids, masked_pos)
        loss_lm = criterion(logits_lm.transpose(1, 2), masked_tokens)  # for masked LM
        loss_lm = (loss_lm.float()).mean()
        loss_clsf = criterion(logits_clsf, isNext)  # for sentence classification
        loss = loss_lm + loss_clsf
        if (epoch + 1) % 10 == 0:
            print("Epoch:", "%04d" % (epoch + 1), "cost =", f"{loss:.6f}")
        loss.backward()
        optimizer.step()

    logger.info("开始使用模型")
    # Predict mask tokens ans isNext
    input_ids, segment_ids, masked_tokens, masked_pos, isNext = map(
        torch.LongTensor, zip(batch[0], strict=False)
    )
    logging.info("训练数据:")
    print(text)
    logging.info("处理的token 列表:")
    print(
        [
            number_dict[w.item()]
            for w in input_ids[0]
            if number_dict[w.item()] != "[PAD]"
        ]
    )

    logits_lm, logits_clsf = model(input_ids, segment_ids, masked_pos)
    logits_lm = logits_lm.data.max(2)[1][0].data.numpy()

    logger.info(
        "这表示在输入序列中被遮蔽（mask）的位置。这些位置的 token 将被模型用来预测 例如 15, 8, 26 是被遮蔽的 token 在输入序列中的索引位置。"
    )
    print(
        "masked tokens list : ",
        [pos.item() for pos in masked_tokens[0] if pos.item() != 0],
    )
    print(
        "对掩码部分预测的结果 它为空（[]），这可能表示模型在当前状态下没有成功预测遮蔽的 \n token predict masked tokens list : ",
        [pos for pos in logits_lm if pos != 0],
    )

    logits_clsf = logits_clsf.data.max(1)[1].data.numpy()[0]
    # isNext 表示实际标签（即真实数据中句子是否相邻）。
    print("isNext : ", True if isNext else False)
    # predict isNext 表示模型的预测结果。
    print("predict isNext : ", True if logits_clsf else False)
