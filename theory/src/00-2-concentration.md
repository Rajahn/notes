# 0.2　集中不等式

## 本节导引

### 这一节要做什么

第 2 章用霍夫丁不等式回答了"一个平均值能偏离期望多远"，并由此得到了 PAC 学习的全部保证。但霍夫丁不等式只用到取值范围。当错误率只有 1% 时，它把每个案例的波动按最坏的 $1/4$ 计算，而真实的方差不到 $0.01$，给出的界松了一个数量级。第 2 章还用到一个没有证明的工具：McDiarmid 不等式。

这一节把集中不等式的工具箱补全：切尔诺夫方法的一般形式、次高斯变量、乘法形式的切尔诺夫界、伯恩斯坦不等式、鞅与 Azuma–Hoeffding 不等式、McDiarmid 不等式的完整证明，最后把它们变成错误率的置信区间。

### 读完这一节，你会知道

1. 切尔诺夫方法为什么是所有指数型集中不等式的共同骨架。
2. 什么是次高斯变量，霍夫丁不等式为什么是它的特例，以及它在方差很小时为什么必然偏松。
3. 乘法形式的切尔诺夫界与伯恩斯坦不等式怎样利用"方差小"，在错误率 1% 时比霍夫丁紧多少（附证明和数字）。
4. 什么是鞅，怎样用"逐个揭晓"的办法证明 McDiarmid 不等式，并用它处理第 2 章的 $\Phi(S)$。
5. 霍夫丁区间、伯恩斯坦区间和精确区间在 $n=400$、错 20 个时分别是多少。

### 本节新词

| 词 | 一句话解释 |
|---|---|
| 矩母函数 | $\mathbb{E}[e^{\lambda X}]$，把随机变量的全部"矩"打包成一个函数 |
| 切尔诺夫方法 | 先取指数再用马尔可夫不等式，最后选最好的 $\lambda$ |
| 次高斯 | 尾部至少像正态分布一样快地变薄的随机变量 |
| 乘法切尔诺夫界 | 用"偏离期望的倍数"表述的 0/1 变量之和的尾部界 |
| 伯恩斯坦不等式 | 同时利用方差和取值上界的集中不等式 |
| 鞅、鞅差 | 逐步揭晓信息时的"当前最佳预测"；每一步预测的修正量 |
| 有界差分 | 改动任何一个参数，函数值的变化都不超过一个常数 |
| McDiarmid 不等式 | 有界差分函数集中在期望附近 |

### 需要的预备知识

- 第 2 章 2.2 节：马尔可夫、切比雪夫、霍夫丁不等式及其证明，特别是霍夫丁引理（引理 2.4）；2.4 节的联合界；2.8 节的 $\Phi(S)$。
- 卷零 0.1 节：独立变量函数的乘积期望（命题 0.1.4），全期望公式（定理 0.1.6）。

---

## 0.2.1 为什么需要集中不等式

**问题**：手头有一个"平均值"，比如测试集上的错误率 $\hat R$。它离我们关心的期望 $R$ 有多远？

第 1 章命题 1.1 只说了 $\hat R$ 平均而言等于 $R$，方差是 $\sigma^2/n$。第 2 章把它变成了概率陈述："偏离超过 $\varepsilon$ 的概率不超过某个数"。这个数越小，样本越少就能给出同样的保证；更关键的是，它要能随 $n$ **指数**下降，才能用联合界同时管住成千上万条候选规则（第 2 章 2.2.3 节）。**集中不等式**就是这类"随机量集中在期望附近"的定量陈述。

最朴素的两个是第 2 章的命题 2.1 和 2.2，这里重述并给出一行证明：

**命题 0.2.1（马尔可夫与切比雪夫）** 若 $Z\ge0$，$a>0$，则 $\Pr(Z\ge a)\le\mathbb{E}[Z]/a$。若 $Z$ 的期望为 $\mu$、方差为 $\sigma^2$，则 $\Pr(\lvert Z-\mu\rvert\ge\varepsilon)\le\sigma^2/\varepsilon^2$。

**证明**：马尔可夫：$Z\ge a\,\mathbf{1}[Z\ge a]$，两边取期望。切比雪夫：对非负量 $(Z-\mu)^2$ 和 $a=\varepsilon^2$ 用马尔可夫。$\square$

切比雪夫利用了方差，但只按 $1/n$ 下降；霍夫丁按 $e^{-n}$ 下降，却不利用方差。这一节的主线是：**怎样两者兼得**。

### 小结

这一节说的是：集中不等式把"平均值接近期望"变成带概率的定量陈述；我们想要的界既要指数下降，又要利用方差。

---

## 0.2.2 切尔诺夫方法

**问题**：第 2 章证明霍夫丁不等式时用了"先取指数、再用马尔可夫"的技巧。这个技巧本身能说出什么？

**定义 0.2.1（矩母函数）** 随机变量 $X$ 的**矩母函数**是 $M_X(\lambda)=\mathbb{E}[e^{\lambda X}]$，$\lambda$ 取使期望有限的实数。

把 $e^{\lambda X}$ 展开成 $1+\lambda X+\lambda^2X^2/2+\cdots$ 就能看到，$M_X$ 里装着 $X$ 的全部矩 $\mathbb{E}[X^k]$，这是名字的由来。

**命题 0.2.2（切尔诺夫方法）** 对任意 $t$ 和任意 $\lambda>0$，

$$
\begin{aligned}
\Pr(X\ge t)&\le e^{-\lambda t}M_X(\lambda),\quad\text{从而}\\
\Pr(X\ge t)&\le\inf_{\lambda>0}e^{-\lambda t}M_X(\lambda).
\end{aligned}
$$

若 $X=\sum_iX_i$ 且各 $X_i$ 相互独立，则 $M_X(\lambda)=\prod_iM_{X_i}(\lambda)$。

**证明**：$\lambda>0$ 时 $X\ge t$ 等价于 $e^{\lambda X}\ge e^{\lambda t}$，对非负量 $e^{\lambda X}$ 用马尔可夫不等式。乘积公式来自命题 0.1.4：独立变量的函数 $e^{\lambda X_i}$ 仍独立，乘积的期望等于期望的乘积。$\square$

**怎么读**：每个 $\lambda$ 都给出一个界，我们挑最小的。下尾 $\Pr(X\le t)$ 对 $-X$ 用同一个命题。之后所有不等式的证明都是这同一个配方，差别只在于**怎样估计 $M_{X_i}(\lambda)$**。

**例子：正态分布**。若 $X\sim N(0,\sigma^2)$，可以算出 $M_X(\lambda)=e^{\lambda^2\sigma^2/2}$。于是 $\Pr(X\ge t)\le\exp(-\lambda t+\lambda^2\sigma^2/2)$，取 $\lambda=t/\sigma^2$ 得

$$
\Pr(X\ge t)\le e^{-t^2/(2\sigma^2)}.
$$

$t=2\sigma$ 时界是 $e^{-2}\approx0.135$，真实值约 0.0228；$t=3\sigma$ 时界是 $e^{-4.5}\approx0.011$，真实值约 0.00135。界的常数偏大，但**指数衰减的速度是对的**，而后面用联合界时，要紧的正是这个速度。

### 小结

这一节说的是：切尔诺夫方法 = 取指数 + 马尔可夫 + 优化 $\lambda$；独立和的矩母函数是乘积；各种集中不等式的区别只在于怎样控制单个变量的矩母函数。

---

## 0.2.3 次高斯随机变量与霍夫丁不等式

**问题**：正态分布的矩母函数是 $e^{\lambda^2\sigma^2/2}$。如果一个随机变量的矩母函数**不超过**这个形式，它的尾部是不是就和正态一样好？

**定义 0.2.2（次高斯）** 设 $\mathbb{E}[X]=\mu$。若对所有实数 $\lambda$，

$$
\mathbb{E}\big[e^{\lambda(X-\mu)}\big]\le e^{\lambda^2\sigma^2/2},
$$

就称 $X$ 是**次高斯**的，$\sigma^2$ 叫作它的**方差代理**。

**命题 0.2.3（次高斯的性质）**

1. 若 $X$ 是方差代理为 $\sigma^2$ 的次高斯变量，则对 $t>0$，$\Pr(X-\mu\ge t)\le e^{-t^2/(2\sigma^2)}$，$\Pr(X-\mu\le-t)\le e^{-t^2/(2\sigma^2)}$。
2. 相互独立的次高斯变量 $X_i$（方差代理 $\sigma_i^2$）之和是次高斯的，方差代理为 $\sum_i\sigma_i^2$。
3. （霍夫丁引理）取值于 $[a,b]$ 的随机变量是次高斯的，方差代理为 $(b-a)^2/4$。

**证明**：(1) 与上一节正态的例子完全相同：切尔诺夫方法取 $\lambda=t/\sigma^2$；下尾对 $-X$ 做。(2) 由命题 0.2.2 的乘积公式，$\prod_ie^{\lambda^2\sigma_i^2/2}=e^{\lambda^2(\sum_i\sigma_i^2)/2}$。(3) 第 2 章引理 2.4 给出 $\mathbb{E}[e^{\lambda(X-\mu)}]\le e^{\lambda^2(b-a)^2/8}$，而 $\frac{(b-a)^2}{8}=\frac12\cdot\frac{(b-a)^2}{4}$。$\square$

三条合起来就是第 2 章定理 2.3：

**定理 0.2.4（霍夫丁不等式，第 2 章定理 2.3）** 设 $Z_1,\dots,Z_n$ 相互独立，$Z_i\in[a_i,b_i]$，$S_n=\sum_iZ_i$。则对 $t>0$，

$$
\Pr\big(S_n-\mathbb{E}S_n\ge t\big)\le\exp\!\left(-\frac{2t^2}{\sum_i(b_i-a_i)^2}\right),
$$

下尾同理。

**怎么读**：由性质 3 和 2，$S_n$ 的方差代理是 $\sum_i(b_i-a_i)^2/4$；代入性质 1，指数是 $-t^2/\big(2\sum_i(b_i-a_i)^2/4\big)=-2t^2/\sum_i(b_i-a_i)^2$。

**次高斯的局限**。方差代理不可能小于真实方差：把 $\mathbb{E}[e^{\lambda(X-\mu)}]=1+\lambda^2\operatorname{Var}[X]/2+\cdots$ 与 $e^{\lambda^2\sigma^2/2}=1+\lambda^2\sigma^2/2+\cdots$ 在 $\lambda\to0$ 时比较即知 $\sigma^2\ge\operatorname{Var}[X]$。更糟的是，对 0/1 变量，最小的方差代理可能远大于方差。以 $\Pr(X=1)=0.01$ 为例：

- 真实方差 $0.01\times0.99=0.0099$；
- 最小的方差代理（可以数值验证，公式为 $\frac{1-2p}{2\ln((1-p)/p)}$）约为 $0.107$；
- 霍夫丁引理用的方差代理是 $1/4$。

原因是这样的变量**尾部不对称**：往上偏离（取到 1）虽然罕见，但一次就偏离 0.99，次高斯的定义要求两个方向、所有 $\lambda$ 都被同一个二次函数压住。要利用"方差小"，必须换一种控制矩母函数的方式。

### 小结

这一节说的是：次高斯变量的矩母函数被正态分布的矩母函数压住，尾部像正态一样薄；有界变量是次高斯的，霍夫丁不等式就是"有界 ⇒ 次高斯 ⇒ 可加 ⇒ 高斯尾"；但方差代理至少是方差，对罕见事件远大于方差。

---

## 0.2.4 乘法形式的切尔诺夫界

**问题**：一条规则的真实错误率是 1%。在 1000 个测试案例上，它的测试错误率达到 2% 以上（即错 20 个以上）的概率有多大？

霍夫丁不等式给出 $e^{-2\times1000\times0.01^2}=e^{-0.2}\approx0.82$，几乎什么也没说。真实概率约 0.0033。下面的界直接针对 0/1 变量之和。

**定理 0.2.5（乘法切尔诺夫界）** 设 $X_1,\dots,X_n$ 相互独立，$X_i\in\{0,1\}$，$\Pr(X_i=1)=p_i$；$X=\sum_iX_i$，$\mu=\mathbb{E}X=\sum_ip_i>0$。则对任意 $t>0$，

$$
\begin{aligned}
\Pr\big(X\ge(1+t)\mu\big)&\le\left(\frac{e^{t}}{(1+t)^{1+t}}\right)^{\mu}\\
&\le\exp\!\left(-\frac{\mu t^2}{2+t}\right);
\end{aligned}
$$

特别地，当 $0<t\le1$ 时右边不超过 $e^{-\mu t^2/3}$。下尾：当 $0<t<1$ 时，$\Pr\big(X\le(1-t)\mu\big)\le e^{-\mu t^2/2}$（练习 0.2.3）。

**怎么读**：$(1+t)\mu$ 是"期望的 $1+t$ 倍"。指数里是 $\mu=np$，**而不是** $n$。代入问题：$\mu=10$，"错 20 个以上"就是 $t=1$，界为 $e^{-10/3}\approx0.036$；第一个更精确的形式给出 $(e/4)^{10}\approx0.021$。比霍夫丁的 0.82 好得多。

#### 证明（第一遍可以跳过）

**思路**：切尔诺夫方法；每个 0/1 变量的矩母函数用 $1+x\le e^x$ 压住；选 $\lambda=\ln(1+t)$；最后一个初等不等式。

1. **单个变量.** $\mathbb{E}[e^{\lambda X_i}]=1-p_i+p_ie^\lambda=1+p_i(e^\lambda-1)\le\exp\big(p_i(e^\lambda-1)\big)$。
2. **乘起来.** 由命题 0.2.2，$\mathbb{E}[e^{\lambda X}]\le\exp\big(\mu(e^\lambda-1)\big)$，所以对 $\lambda>0$：

$$
\Pr\big(X\ge(1+t)\mu\big)\le\exp\big(-\lambda(1+t)\mu+\mu(e^\lambda-1)\big).
$$

3. **选 $\lambda$.** 取 $\lambda=\ln(1+t)>0$（这正是让指数最小的值），$e^\lambda-1=t$，指数变为 $\mu\big(t-(1+t)\ln(1+t)\big)$，这就是第一个不等式。
4. **化简.** 只需证明对 $t\ge0$，$(1+t)\ln(1+t)-t\ge\frac{t^2}{2+t}$。先证 $\ln(1+t)\ge\frac{2t}{2+t}$：令 $u(t)=\ln(1+t)-\frac{2t}{2+t}$，$u(0)=0$，

$$
\begin{aligned}
u'(t)&=\frac1{1+t}-\frac{4}{(2+t)^2}=\frac{(2+t)^2-4(1+t)}{(1+t)(2+t)^2}\\
&=\frac{t^2}{(1+t)(2+t)^2}\ge0 .
\end{aligned}
$$

   于是 $(1+t)\ln(1+t)-t\ge\frac{2t(1+t)}{2+t}-t=\frac{t^2}{2+t}$。
5. **$t\le1$ 时**，$2+t\le3$，所以 $\frac{t^2}{2+t}\ge\frac{t^2}{3}$。$\square$

**为什么比霍夫丁紧这么多？** 把两者都写成"测得错误率 $\hat p$ 比真实 $p$ 高出 $\varepsilon$"的形式。霍夫丁是 $e^{-2n\varepsilon^2}$；乘法切尔诺夫取 $t=\varepsilon/p$，是 $e^{-n\varepsilon^2/(3p)}$（$\varepsilon\le p$ 时）。指数之比是 $\frac{1}{3p}:2$，$p=0.01$ 时约 17 倍。原因是 0/1 变量的方差 $p(1-p)\approx p$，切尔诺夫界的分母里出现的正是这个量级。

**需要多少样本**：要让"真实 1% 的规则测出 2% 以上"的概率不超过 5%：

- 霍夫丁：$e^{-2n\times0.0001}\le0.05$，需要 $n\ge\ln20/0.0002\approx14\,979$；
- 乘法切尔诺夫（$e^{-\mu/3}$ 形式）：$np/3\ge\ln20$，需要 $n\ge899$；用更精确的形式只要 $n\ge776$。

### 小结

这一节说的是：对 0/1 变量之和，乘法切尔诺夫界的指数正比于期望 $\mu=np$ 而不是 $n$；错误率小时它比霍夫丁紧一个数量级以上，所需样本从约 15 000 降到约 900。

---

## 0.2.5 伯恩斯坦不等式

**问题**：乘法切尔诺夫界只适用于 0/1 变量，而且是"相对偏离"的形式。能不能对一般的有界变量，同时利用方差和指数下降？第 2 章练习 2.5 承诺的正是这个。

**定理 0.2.6（伯恩斯坦不等式）** 设 $X_1,\dots,X_n$ 相互独立，$X_i-\mathbb{E}X_i\le M$，$v=\sum_i\operatorname{Var}[X_i]$，$S=\sum_iX_i$。则对 $t>0$，

$$
\Pr\big(S-\mathbb{E}S\ge t\big)\le\exp\!\left(-\frac{t^2}{2\,(v+Mt/3)}\right).
$$

下尾对 $-X_i$ 使用，条件变为 $\mathbb{E}X_i-X_i\le M$。

**怎么读**：

- 分母有两项。$t$ 较小时 $v$ 占主导，界约为 $e^{-t^2/(2v)}$，就像方差为 $v$ 的正态分布，**用的是真实方差**而不是最坏的范围；$t$ 较大时 $Mt/3$ 占主导，界约为 $e^{-3t/(2M)}$，是指数尾。
- 平均值形式：独立同分布、单个方差 $\sigma^2$ 时，$v=n\sigma^2$，取 $t=n\varepsilon$：

$$
\Pr\big(\bar X-\mu\ge\varepsilon\big)\le\exp\!\left(-\frac{n\varepsilon^2}{2(\sigma^2+M\varepsilon/3)}\right).
$$

- 反解成区间：记 $L=\ln(1/\delta)$，则以至少 $1-\delta$ 的概率

$$
\bar X-\mu<\sqrt{\frac{2\sigma^2L}{n}}+\frac{2ML}{3n}.
$$

  （验证：令 $t_0=\sqrt{2vL}+2ML/3$，展开可得 $t_0^2-2L(v+Mt_0/3)=\frac23ML\sqrt{2vL}\ge0$，所以 $t_0$ 处的界不超过 $e^{-L}=\delta$；再除以 $n$。）

**代入数字**：$p=0.01$，$\sigma^2=0.0099$，$M=0.99$，$n=1000$，$\varepsilon=0.01$：

$$
\exp\!\left(-\frac{1000\times0.0001}{2(0.0099+0.0033)}\right)=e^{-3.79}\approx0.023 .
$$

#### 证明（第一遍可以跳过）

**思路**：还是切尔诺夫方法。关键是下面的引理：一个上有界、方差为 $\sigma^2$ 的中心化变量，矩母函数的对数被一个含 $\sigma^2$ 的量压住。

**引理 0.2.7** 设 $\mathbb{E}[Y]=0$，$Y\le M$（$M>0$），$\mathbb{E}[Y^2]=\sigma^2$。则对 $0<\lambda<3/M$，

$$
\ln\mathbb{E}\big[e^{\lambda Y}\big]\le\frac{\lambda^2\sigma^2}{2(1-\lambda M/3)}.
$$

**引理的证明.**

1. **一个递增函数.** 令 $g(u)=(e^u-1-u)/u^2$（$g(0)=1/2$）。由泰勒公式的积分余项，$e^u-1-u=u^2\int_0^1(1-s)e^{su}\,ds$，即 $g(u)=\int_0^1(1-s)e^{su}\,ds$。对每个 $s\in[0,1]$，$e^{su}$ 随 $u$ 递增，所以 $g$ 在整条实轴上递增。
2. **压住指数.** $e^{\lambda Y}=1+\lambda Y+\lambda^2Y^2g(\lambda Y)$。由于 $\lambda Y\le\lambda M$、$g$ 递增、$Y^2\ge0$：$e^{\lambda Y}\le1+\lambda Y+\lambda^2Y^2g(\lambda M)$。
3. **取期望.** 用 $\mathbb{E}Y=0$、$\mathbb{E}Y^2=\sigma^2$：$\mathbb{E}[e^{\lambda Y}]\le1+\lambda^2\sigma^2g(\lambda M)$。
4. **估计 $g$.** 对 $0\le u<3$，用 $k!\ge2\cdot3^{k-2}$（$k\ge2$，归纳可证）：

$$
\begin{aligned}
e^u-1-u&=\sum_{k\ge2}\frac{u^k}{k!}\le\frac{u^2}{2}\sum_{k\ge2}\Big(\frac u3\Big)^{k-2}\\
&=\frac{u^2}{2(1-u/3)},
\end{aligned}
$$

   即 $g(u)\le\frac{1}{2(1-u/3)}$。代入 $u=\lambda M$，再用 $1+x\le e^x$ 后取对数即得引理。$\square$

**定理的证明.** 对 $Y_i=X_i-\mathbb{E}X_i$ 用引理，各 $\sigma_i^2$ 相加为 $v$。由命题 0.2.2，对 $0<\lambda<3/M$：

$$
\Pr\big(S-\mathbb{E}S\ge t\big)\le\exp\!\left(-\lambda t+\frac{\lambda^2v}{2(1-\lambda M/3)}\right).
$$

取 $\lambda=\dfrac{t}{v+Mt/3}$。它满足 $\lambda M<3$，并且 $1-\lambda M/3=\dfrac{v}{v+Mt/3}$，所以

$$
\begin{aligned}
-\lambda t+\frac{\lambda^2v}{2(1-\lambda M/3)}
&=-\frac{t^2}{v+Mt/3}+\frac{t^2}{2(v+Mt/3)}\\
&=-\frac{t^2}{2(v+Mt/3)}.\qquad\square
\end{aligned}
$$

**和霍夫丁、切比雪夫比较**（第 2 章练习 2.5 的承诺）。仍取错误率 $p=0.01$、$n=1000$。先看"测得错误率比真实高出 0.01 以上"的概率上界：

| 方法 | 用到的信息 | 上界 |
|---|---|---|
| 霍夫丁 | 取值范围 $[0,1]$ | 0.819 |
| 切比雪夫 | 方差 0.0099 | 0.099 |
| 伯恩斯坦 | 方差 + 上界 $M=0.99$ | 0.023 |
| 乘法切尔诺夫（精确形式） | 0/1 变量的全部分布 | 0.021 |
| 精确二项概率 | — | 0.0033 |

再看反过来的问题：给定把握 $1-\delta$，偏离的半径 $\varepsilon$ 能做到多小（单侧；伯恩斯坦用上面的区间公式，取 $M=0.99$ 时两个方向都适用；切比雪夫半径为 $\sqrt{\sigma^2/(n\delta)}$）：

| $\delta$ | 霍夫丁 | 切比雪夫 | 伯恩斯坦 |
|---|---|---|---|
| 0.05 | 0.0387 | 0.0141 | 0.0097 |
| 0.001 | 0.0588 | 0.0995 | 0.0163 |
| $10^{-6}$ | 0.0831 | 3.15（无意义） | 0.0257 |

切比雪夫利用了方差，在 $\delta=0.05$ 时比霍夫丁好，但 $\delta$ 变小后按 $1/\sqrt\delta$ 爆炸；霍夫丁按 $\sqrt{\ln(1/\delta)}$ 缓慢增长，却从一开始就宽；伯恩斯坦两头都占。$\delta$ 很小正是联合界需要的情形（0.2.8 节）。

**一个实际的困难**：伯恩斯坦不等式要知道真实方差 $\sigma^2$，而它通常未知。两种常见的处理：用样本方差代替真实方差，付出稍大的常数（**经验伯恩斯坦不等式**，Maurer 与 Pontil 2009；Audibert 等 2009）；或者像 0.2.9 节那样，对每个候选的 $p$ 分别检验，此时方差 $p(1-p)$ 是已知的。

### 小结

这一节说的是：伯恩斯坦不等式的分母是"方差 + 上界 × 偏离 / 3"，偏离小时像用真实方差的正态尾，偏离大时是指数尾；错误率 1% 时它的半径只有霍夫丁的三分之一到四分之一，而且在 $\delta$ 很小时不像切比雪夫那样崩溃。

---

## 0.2.6 鞅与 Azuma–Hoeffding 不等式

**问题**：第 2 章的 $\Phi(S)=\sup_g\big(\mathbb{E}[g]-\hat{\mathbb{E}}_S[g]\big)$ 不是独立变量之和，前面的方法都用不上。怎样处理"依赖于很多独立输入、但不是和"的量？

**想法：逐个揭晓**。设 $f(Z_1,\dots,Z_n)$ 是 $n$ 个独立案例的某个函数。设想案例一个一个揭晓。在看到前 $k$ 个之后，对 $f$ 的"当前最佳预测"是把未揭晓的案例平均掉：

$$
\begin{aligned}
M_k&=g_k(Z_1,\dots,Z_k),\\
g_k(z_1,\dots,z_k)&=\mathbb{E}\big[f(z_1,\dots,z_k,Z_{k+1},\dots,Z_n)\big].
\end{aligned}
$$

$M_0=\mathbb{E}[f]$（什么都没看到），$M_n=f(Z_1,\dots,Z_n)$（全部看到）。第 $k$ 个案例揭晓带来的修正是 $D_k=M_k-M_{k-1}$，于是

$$
f-\mathbb{E}f=M_n-M_0=\sum_{k=1}^nD_k .
$$

**例子**：$f$ 是错误个数 $\sum_iX_i$，$\Pr(X_i=1)=p$。看到前 $k$ 个之后的最佳预测是"已看到的错误数 + $(n-k)p$"，修正量 $D_k=X_k-p$。这就是普通的中心化求和。一般的 $f$ 不是和，但仍然可以写成修正量之和。

修正量有一个关键性质：**在已知前 $k-1$ 个案例时，它的平均为 0**。直观地说，$M_{k-1}$ 已经是把第 $k$ 个案例平均掉的结果，揭晓之前不可能预料修正的方向。

**定义 0.2.3（鞅差序列）** 设 $D_k$ 是 $Z_1,\dots,Z_k$ 的函数（$k=1,\dots,n$）。如果对每个 $k$ 和前 $k-1$ 个变量的每一组取值，$\mathbb{E}[D_k\mid Z_1,\dots,Z_{k-1}]=0$，就称 $D_1,\dots,D_n$ 是**鞅差序列**；部分和 $M_k=M_0+\sum_{j\le k}D_j$ 叫作**鞅**。上面由 $f$ 构造的 $M_k$ 叫作 **Doob 鞅**。

**类比与局限**：鞅常被比作"公平赌博中的累计输赢"，每一局的期望收益为 0，但下注的大小可以依赖于前面的结果。这个类比的局限是：在 Doob 鞅里没有人在"下注"，修正量完全由 $f$ 和已揭晓的数据决定。

**定理 0.2.8（Azuma–Hoeffding 不等式）** 设 $D_1,\dots,D_n$ 是关于 $Z_1,\dots,Z_n$ 的鞅差序列，并且对每个 $k$，在前 $k-1$ 个变量取定的条件下，$D_k$ 落在一个长度不超过 $c_k$ 的区间里（区间的位置可以依赖于 $Z_1,\dots,Z_{k-1}$）。则对 $t>0$，

$$
\Pr\Big(\sum_{k=1}^nD_k\ge t\Big)\le\exp\!\left(-\frac{2t^2}{\sum_kc_k^2}\right).
$$

**怎么读**：形式和霍夫丁不等式一模一样，只是"独立有界变量"换成了"条件平均为 0、条件范围有界的修正量"。若只知道 $\lvert D_k\rvert\le c_k$，区间长度是 $2c_k$，界变成 Azuma 最初的形式 $e^{-t^2/(2\sum_kc_k^2)}$（练习 0.2.6）。

#### 证明（第一遍可以跳过）

**思路**：和霍夫丁不等式一样，只是"独立性拆乘积"换成"用全期望公式一层一层剥"。

1. **条件霍夫丁引理.** 取定 $Z_1,\dots,Z_{k-1}$ 的值后，$D_k$ 的条件分布平均为 0、取值范围长度不超过 $c_k$。对这个条件分布用第 2 章引理 2.4：$\mathbb{E}\big[e^{\lambda D_k}\mid Z_1,\dots,Z_{k-1}\big]\le e^{\lambda^2c_k^2/8}$。
2. **剥掉最后一层.** 记 $T_k=\sum_{j\le k}D_j$。$T_{n-1}$ 只依赖于 $Z_1,\dots,Z_{n-1}$，取定这些值时它是常数。由全期望公式（定理 0.1.6），

$$
\begin{aligned}
\mathbb{E}\big[e^{\lambda T_n}\big]&=\mathbb{E}\Big[e^{\lambda T_{n-1}}\,\mathbb{E}\big[e^{\lambda D_n}\mid Z_1,\dots,Z_{n-1}\big]\Big]\\
&\le e^{\lambda^2c_n^2/8}\,\mathbb{E}\big[e^{\lambda T_{n-1}}\big].
\end{aligned}
$$

3. **重复.** 对 $T_{n-1},T_{n-2},\dots$ 依次这样做，得 $\mathbb{E}[e^{\lambda T_n}]\le\exp\big(\lambda^2\sum_kc_k^2/8\big)$。
4. **切尔诺夫.** 与第 2 章 2.2.5 节第四步完全相同，取 $\lambda=4t/\sum_kc_k^2$，得到 $e^{-2t^2/\sum_kc_k^2}$。$\square$

### 小结

这一节说的是：把一个依赖于 $n$ 个独立输入的量看成"逐个揭晓时的预测修正之和"，修正量条件平均为 0，这就是鞅差；只要每一步修正的范围有界，就有和霍夫丁一样的指数界。

---

## 0.2.7 McDiarmid 不等式

**问题**：什么样的函数，其 Doob 鞅的每一步修正范围有界？

**定义 0.2.4（有界差分）** 函数 $f(z_1,\dots,z_n)$ 满足**有界差分**条件（常数 $c_1,\dots,c_n$），如果对每个 $i$，只改变第 $i$ 个参数时函数值的变化不超过 $c_i$：

$$
\lvert f(z_1,\dots,z_i,\dots,z_n)-f(z_1,\dots,z_i',\dots,z_n)\rvert\le c_i .
$$

**例子**：$n$ 个取值于 $[0,C]$ 的数的平均值，改一个数最多变化 $C/n$，所以 $c_i=C/n$。

**定理 0.2.9（McDiarmid 不等式）** 设 $Z_1,\dots,Z_n$ 相互独立（各自可以取值于任意集合），$f$ 满足常数为 $c_i$ 的有界差分条件。则对 $t>0$，

$$
\Pr\big(f(Z_1,\dots,Z_n)-\mathbb{E}f\ge t\big)\le\exp\!\left(-\frac{2t^2}{\sum_ic_i^2}\right),
$$

对 $\mathbb{E}f-f$ 同样成立，两侧合起来乘 2。

**怎么读**：$f$ 不必是和，只要"没有哪个案例能单独把它拉动太多"。平均值的情形 $\sum_ic_i^2=C^2/n$，退化为霍夫丁不等式。

#### 证明（第一遍可以跳过）

**思路**：构造 Doob 鞅，验证两件事：修正量条件平均为 0（用独立性），每步修正落在长度 $\le c_k$ 的区间里（用有界差分）；然后套 Azuma–Hoeffding。

沿用上一节的 $g_k$、$M_k$、$D_k$，已知 $f-\mathbb{E}f=\sum_kD_k$。

1. **条件平均为 0.** 取定 $z_1,\dots,z_{k-1}$。由于 $Z_k$ 与前面的变量独立，它的条件分布就是它自己的分布，所以

$$
\begin{aligned}
\mathbb{E}\big[g_k(z_1,\dots,z_{k-1},Z_k)\big]&=\mathbb{E}\big[f(z_1,\dots,z_{k-1},Z_k,\dots,Z_n)\big]\\
&=g_{k-1}(z_1,\dots,z_{k-1}).
\end{aligned}
$$

   第一个等号把"先对 $Z_{k+1},\dots,Z_n$ 平均、再对 $Z_k$ 平均"合并成对 $Z_k,\dots,Z_n$ 一起平均，这一步用到 $Z_k$ 与后面的变量独立。于是 $\mathbb{E}[D_k\mid Z_1,\dots,Z_{k-1}]=0$。
2. **修正范围有界.** 仍取定 $z_1,\dots,z_{k-1}$，让第 $k$ 个参数取两个值 $z,z'$：

$$
\begin{aligned}
&g_k(z_1,\dots,z_{k-1},z)-g_k(z_1,\dots,z_{k-1},z')\\
&\quad=\mathbb{E}\big[f(z_1,\dots,z,\dots,Z_n)-f(z_1,\dots,z',\dots,Z_n)\big]\le c_k .
\end{aligned}
$$

   期望里的差对每一组 $Z_{k+1},\dots,Z_n$ 的取值都不超过 $c_k$。所以当 $z$ 变化时，$g_k(z_1,\dots,z_{k-1},z)$ 落在一个区间 $[L_k,U_k]$ 里，$U_k-L_k\le c_k$，而 $L_k,U_k$ 只依赖于 $z_1,\dots,z_{k-1}$。于是 $D_k=g_k-g_{k-1}$ 落在 $[L_k-g_{k-1},U_k-g_{k-1}]$，长度不超过 $c_k$，位置只依赖于前 $k-1$ 个变量。
3. **套用定理 0.2.8**，得到上尾的界。对 $-f$（有界差分常数相同）做一遍得到下尾。$\square$

**独立性用在哪里**：第 1 步。如果 $Z_k$ 与前面的案例相关（比如同一订单的多次售后），揭晓 $Z_1,\dots,Z_{k-1}$ 会改变 $Z_k$ 的分布，$g_k$ 的定义和第 1 步都要改写，界一般不再成立。

### 例子：第 2 章的 $\Phi(S)$

**命题 0.2.10** 设 $\mathcal{G}$ 是一族取值于 $[0,1]$ 的函数，$\Phi(S)=\sup_{g\in\mathcal{G}}\big(\mathbb{E}[g]-\hat{\mathbb{E}}_S[g]\big)$，其中 $\hat{\mathbb{E}}_S[g]=\frac1n\sum_ig(z_i)$。则 $\Phi$ 满足常数 $c_i=1/n$ 的有界差分条件。因此以至少 $1-\delta$ 的概率，

$$
\Phi(S)\le\mathbb{E}[\Phi(S)]+\sqrt{\frac{\ln(1/\delta)}{2n}}.
$$

**证明**：设 $S'$ 与 $S$ 只在第 $i$ 个点不同。对每个 $g$，$\hat{\mathbb{E}}_S[g]$ 与 $\hat{\mathbb{E}}_{S'}[g]$ 只差一项，最多差 $1/n$，所以

$$
\begin{aligned}
\mathbb{E}[g]-\hat{\mathbb{E}}_S[g]&\le\mathbb{E}[g]-\hat{\mathbb{E}}_{S'}[g]+\frac1n\\
&\le\Phi(S')+\frac1n .
\end{aligned}
$$

对左边取上确界得 $\Phi(S)\le\Phi(S')+1/n$；交换 $S,S'$ 得另一个方向。再用定理 0.2.9：$\sum_ic_i^2=1/n$，令 $e^{-2nt^2}=\delta$ 解出 $t$。$\square$

这正是第 2 章定理 2.14 证明的第 1 步。**代入数字**：$n=400$、$\delta=0.05$ 时，偏离不超过 $\sqrt{\ln20/800}\approx0.061$。值得注意的是，$\Phi(S)$ 是对可能无穷多个函数取上确界，它的集中程度却和**一个**平均值一样好。难的部分是它的期望 $\mathbb{E}[\Phi(S)]$，第 2 章用 Rademacher 复杂度控制。

### 小结

这一节说的是：McDiarmid 不等式说，任何"改动一个输入只能改变一点"的函数都集中在期望附近；证明是构造 Doob 鞅，用独立性得到条件平均为 0，用有界差分得到每步范围有界，再套 Azuma–Hoeffding。

---

## 0.2.8 联合界：从一条规则到很多条

**问题**：上面的不等式都关于**一个**随机量。要同时管住 $k$ 条候选规则，怎么办？

第 2 章命题 2.6 的联合界说 $\Pr(A_1\cup\dots\cup A_k)\le\sum_j\Pr(A_j)$。做法永远是：给每条规则分配 $\delta/k$ 的"出意外额度"，即把单条规则界里的 $\ln(1/\delta)$ 换成 $\ln(k/\delta)$。这一步不需要规则之间独立。

**集中不等式的形状在这里起决定作用**。仍以第 2 章的 81 000 条候选规则、$n=1000$、$\delta=0.05$ 为例，$\ln(81\,000/0.05)\approx14.3$。对一条真实错误率为 1% 的规则：

- 霍夫丁半径：$\sqrt{14.3/2000}\approx0.085$；
- 伯恩斯坦半径（$\sigma^2=0.0099$，$M=0.99$）：$\sqrt{2\times0.0099\times14.3/1000}+\frac{2\times0.99\times14.3}{3000}\approx0.026$；
- 切比雪夫半径：$\sqrt{0.0099\times81\,000/(1000\times0.05)}\approx4.0$，毫无意义。

伯恩斯坦界的第二项按 $\ln(k/\delta)/n$ 增长，而不是 $\sqrt{\ln(k/\delta)/n}$。当规则的错误率很小时，样本复杂度从不可知情形的 $1/\varepsilon^2$ 量级向可实现情形（第 2 章定理 2.9）的 $1/\varepsilon$ 量级靠拢。注意这里每条规则用的是它自己的方差 $\sigma_h^2$，它是固定的常数，所以联合界照常成立；但 $\sigma_h^2$ 未知，实际使用时要换成经验伯恩斯坦界。

### 小结

这一节说的是：联合界把 $\ln(1/\delta)$ 换成 $\ln(k/\delta)$；对错误率小的规则，伯恩斯坦界在联合界下的代价远小于霍夫丁，切比雪夫则完全失效。

---

## 0.2.9 从不等式到错误率的置信区间

**问题**：测试集有 $n=400$ 个案例，规则错了 $k=20$ 个，$\hat p=0.05$。真实错误率的 95% 区间是什么？

**霍夫丁区间**。由定理 0.2.4 的两侧形式，以至少 $1-\delta$ 的概率 $\lvert\hat p-p\rvert<\sqrt{\ln(2/\delta)/(2n)}$。$\delta=0.05$ 时半径 $\sqrt{\ln40/800}\approx0.068$，区间 $[0,0.118]$（下端截到 0）。它对任何 $n$、任何 $p$ 都成立，但很宽：它按方差 $1/4$ 计算，而 $p$ 在 0.05 附近时方差只有约 0.0475。

**伯恩斯坦区间（逐个检验）**。换个思路：对每个**候选**的真实错误率 $p$，如果真值是 $p$，方差 $p(1-p)$ 就是已知的。用伯恩斯坦不等式检验"观察到 $\hat p=0.05$ 是否离 $p$ 太远"，两侧各用 $\delta/2$，保留没有被否定的 $p$。若真值为 $p$，它被否定的概率不超过 $\delta$，所以保留下来的集合是一个合法的 95% 区间。算出来是 $[0.025,0.089]$。（$p<\hat p$ 时检验上尾，$M=1-p$；$p>\hat p$ 时检验下尾，$M=p$。）

**精确区间**。把伯恩斯坦界换成精确的二项尾概率，同样逐个检验，得到 Clopper–Pearson 区间 $[0.031,0.076]$。

| 方法 | 95% 区间 | 宽度 | 保证 |
|---|---|---|---|
| 正态近似（0.1 节） | $[0.029,0.071]$ | 0.043 | 无；$p=0.05$ 时实际覆盖约 92.7% |
| 霍夫丁 | $[0,0.118]$ | 0.118 | 对所有 $n,p$ 成立 |
| 伯恩斯坦（逐个检验） | $[0.025,0.089]$ | 0.064 | 对所有 $n,p$ 成立 |
| 精确（Clopper–Pearson） | $[0.031,0.076]$ | 0.045 | 对所有 $n,p$ 成立 |

如果只关心上界（"真实错误率不超过多少"），单侧 95%：霍夫丁给出 $0.05+\sqrt{\ln20/800}\approx0.111$，精确方法给出约 0.072。

**怎么选**：报告单条规则在测试集上的错误率时，用精确区间；需要同时处理很多条规则、或者被估计的量不是简单的比例（如 $\Phi(S)$）时，用集中不等式；正态近似只在 $n\hat p$ 和 $n(1-\hat p)$ 都不小时作为粗略参考。"逐个检验再保留"的构造方法和精确区间的细节，后面讲统计推断时会讲。

### 小结

这一节说的是：集中不等式反解出的区间对任何样本量都成立；霍夫丁区间在错误率小时比精确区间宽一倍多，利用方差的伯恩斯坦区间介于两者之间。

---

## 0.2.10 这一节在全书中的位置

| 本节结论 | 在"语言模型读事实、规则做判定"的系统里意味着什么 |
|---|---|
| 切尔诺夫方法 | 所有"以高概率"保证的共同骨架 |
| 乘法切尔诺夫、伯恩斯坦 | 错误率小时，验证一条规则需要的测试案例比霍夫丁估计的少一个数量级 |
| McDiarmid 不等式 | 不是平均值的量（最大偏差、碰撞下界、选出的规则的成绩）也能有集中保证，前提是案例独立 |
| 独立性的作用 | 同源案例会破坏所有这些界；划分数据时要整组放在一边 |
| 联合界 + 伯恩斯坦 | 比较很多候选时，罕见错误的规则付出的"多重比较代价"更小 |
| 置信区间 | 报告测试错误率时用精确区间；霍夫丁区间可靠但宽 |

---

## 0.2.11 本节小结

- 切尔诺夫方法：$\Pr(X\ge t)\le\inf_{\lambda>0}e^{-\lambda t}\mathbb{E}[e^{\lambda X}]$；独立和的矩母函数是乘积（命题 0.2.2）。
- 次高斯变量有正态式的尾部；有界 ⇒ 次高斯（霍夫丁引理），由此得到霍夫丁不等式（命题 0.2.3、定理 0.2.4）。但方差代理至少是方差，罕见事件时远大于方差。
- 乘法切尔诺夫界的指数正比于 $\mu=np$；$p=0.01$ 时所需样本约为霍夫丁的 $1/17$（定理 0.2.5）。
- 伯恩斯坦不等式 $\exp\big(-t^2/(2(v+Mt/3))\big)$，同时利用方差和指数下降（定理 0.2.6、引理 0.2.7）。
- Doob 鞅把函数写成修正量之和；Azuma–Hoeffding 对鞅差给出霍夫丁式的界（定理 0.2.8）；McDiarmid 不等式对有界差分函数成立（定理 0.2.9），$\Phi(S)$ 的 $c_i=1/n$（命题 0.2.10）。
- $n=400$、$k=20$：霍夫丁 $[0,0.118]$，伯恩斯坦 $[0.025,0.089]$，精确 $[0.031,0.076]$。

---

## 练习

难度标记：★ 检验理解，★★ 需要推导或计算，★★★ 开放思考。

**练习 0.2.1** ★ 一条规则的真实错误率为 2%，测试集 $n=500$。分别用霍夫丁不等式和乘法切尔诺夫界（$e^{-\mu t^2/3}$ 形式）估计"测试错误率达到 4% 以上"的概率，并解释差距的来源。

**练习 0.2.2** ★ 下列函数的有界差分常数 $c_i$ 是多少？McDiarmid 不等式对它们有用吗？（a）$n$ 个 $[0,C]$ 中的数的平均值；（b）$n$ 个 $[0,1]$ 中的数的最大值；（c）$n$ 个案例中不同"事实组合"的个数。

**练习 0.2.3** ★★ 证明乘法切尔诺夫界的下尾：$0<t<1$ 时，$\Pr(X\le(1-t)\mu)\le e^{-\mu t^2/2}$。（提示：对 $-X$ 用切尔诺夫方法，取 $\lambda=-\ln(1-t)$，再证明 $(1-t)\ln(1-t)+t\ge t^2/2$。）

**练习 0.2.4** ★★ 第 1 章命题 1.9 的碰撞下界 $L_\phi(S)=\frac1n\sum_j\min_\ell\sum_{i\in G_j}c(y_i,\ell)$，代价取值于 $[0,C]$。证明它作为 $n$ 个案例的函数满足 $c_i=C/n$ 的有界差分条件，并写出它的集中不等式。$n=400$、0-1 代价、$\delta=0.05$ 时偏离不超过多少？这个结论能否说明碰撞下界是将来最好成绩的好估计？

**练习 0.2.5** ★★ 一条规则的真实错误率约为 2%。要以 95% 的把握保证测得的错误率与真实值相差不超过 0.01（单侧），霍夫丁不等式和伯恩斯坦不等式（取 $\sigma^2=0.0196$，$M=0.98$）分别需要多少测试案例？

**练习 0.2.6** ★★ 在 McDiarmid 不等式的证明中，说明 $\lvert D_k\rvert\le c_k$ 也成立。如果只用这个事实，配合 Azuma 的原始形式 $e^{-t^2/(2\sum_kc_k^2)}$，得到的界比定理 0.2.9 差多少？

**练习 0.2.7** ★★★ 一个团队在同一个测试集（$n=2000$）上比较 30 个提示词，最好的那个错了 18 个。他们想报告一个可信的错误率上界。比较几种方案：霍夫丁 + 联合界、伯恩斯坦 + 联合界（方差怎么办？）、精确二项 + 联合界、另留一份数据。各自的前提和代价是什么？

---

## 练习提示与答案

<details>
<summary>练习 0.2.1</summary>

霍夫丁：$e^{-2\times500\times0.02^2}=e^{-0.4}\approx0.67$。乘法切尔诺夫：$\mu=10$，$t=1$，$e^{-10/3}\approx0.036$（精确形式 $(e/4)^{10}\approx0.021$）。精确二项概率约 0.0031。

差距来自方差：霍夫丁按取值范围 $[0,1]$ 计算，相当于假设方差为 $1/4$；切尔诺夫界的指数里是 $\mu=np$，反映了真实方差 $p(1-p)\approx0.02$。

</details>

<details>
<summary>练习 0.2.2</summary>

（a）$c_i=C/n$，$\sum c_i^2=C^2/n$，就是霍夫丁不等式，很有用。

（b）改一个数，最大值最多变化 1，$c_i=1$，$\sum c_i^2=n$，界为 $e^{-2t^2/n}$，$t<1$ 时几乎没用。最大值的集中需要别的工具。

（c）改一个案例，不同组合的个数最多变化 1，$c_i=1$，界为 $e^{-2t^2/n}$。它说个数的偏离是 $\sqrt n$ 量级，对计数本身（可达 $n$）有用；除以 $n$ 后就是"不同组合的比例"，$c_i=1/n$，偏离是 $1/\sqrt n$ 量级。

</details>

<details>
<summary>练习 0.2.3</summary>

对 $\lambda>0$：$\Pr(X\le(1-t)\mu)=\Pr(e^{-\lambda X}\ge e^{-\lambda(1-t)\mu})\le e^{\lambda(1-t)\mu}\mathbb{E}[e^{-\lambda X}]$。与上尾证明的第 1 步相同，$\mathbb{E}[e^{-\lambda X}]\le\exp(\mu(e^{-\lambda}-1))$。取 $\lambda=-\ln(1-t)>0$，$e^{-\lambda}-1=-t$，指数为 $\mu\big(-(1-t)\ln(1-t)-t\big)$。

令 $w(t)=(1-t)\ln(1-t)+t-t^2/2$，$w(0)=0$，$w'(t)=-\ln(1-t)-t\ge0$（因为 $-\ln(1-t)\ge t$）。所以 $(1-t)\ln(1-t)+t\ge t^2/2$，指数不超过 $-\mu t^2/2$。

</details>

<details>
<summary>练习 0.2.4</summary>

把第 $i$ 个案例换掉，等价于先从它原来的组里删掉、再加到新的组里（可能是同一组）。从一组删掉一个案例时，组内每个候选结论 $\ell$ 的代价和减少 $c(y_i,\ell)\in[0,C]$，所以最小值减少的量在 $[0,C]$ 里；加入一个案例时，最小值增加的量在 $[0,C]$ 里。两步合起来，$n\cdot L_\phi$ 的变化在 $[-C,C]$ 里，即 $c_i=C/n$。

由 McDiarmid 不等式，$\Pr(\lvert L_\phi(S)-\mathbb{E}L_\phi(S)\rvert\ge t)\le2e^{-2nt^2/C^2}$。$n=400$、$C=1$、$\delta=0.05$：$t=\sqrt{\ln40/800}\approx0.068$。

不能。它只说明 $L_\phi(S)$ 集中在**它自己的期望**附近；而第 1 章 1.10.3 节指出，这个期望本身偏乐观（低于用 $\phi$ 能达到的最低真实风险）。集中与无偏是两回事。

</details>

<details>
<summary>练习 0.2.5</summary>

$L=\ln20\approx3.0$，$\varepsilon=0.01$。

- 霍夫丁：$n\ge L/(2\varepsilon^2)\approx14\,979$。
- 伯恩斯坦：$n\varepsilon^2/(2(\sigma^2+M\varepsilon/3))\ge L$，即 $n\ge2L(0.0196+0.00327)/0.0001\approx1370$。

伯恩斯坦需要的案例约为霍夫丁的 $1/11$。

</details>

<details>
<summary>练习 0.2.6</summary>

$D_k$ 的条件平均为 0，而它落在长度不超过 $c_k$ 的区间里，所以这个区间包含 0，区间内任何一点到 0 的距离不超过 $c_k$，即 $\lvert D_k\rvert\le c_k$。

只用 $\lvert D_k\rvert\le c_k$，区间长度按 $2c_k$ 算，得到 $e^{-t^2/(2\sum c_k^2)}$，指数是定理 0.2.9 的 $1/4$。要达到同样的把握，偏离量要放大一倍，或者样本数要多四倍。

</details>

<details>
<summary>练习 0.2.7</summary>

开放问题，参考思路：

- 测试集参与了 30 选 1，最好那个的成绩偏乐观，必须按 30 次比较放宽：把 $\delta$ 换成 $\delta/30$。
- 霍夫丁 + 联合界：单侧半径 $\sqrt{\ln(600)/4000}\approx0.040$，上界约 $0.009+0.040=0.049$，可靠但宽。
- 伯恩斯坦 + 联合界：每个提示词的方差未知。可以用经验伯恩斯坦界，或对每个候选 $p$ 做逐个检验（方差 $p(1-p)$ 已知），再套联合界。
- 精确二项 + 联合界：对最好那个取 $\delta/30$ 水平的 Clopper–Pearson 单侧上界。这是"比较 30 个"情形下最紧的通用做法之一。
- 另留一份数据：只评估最终选中的那一个，不需要联合界；代价是数据被分走。后面讲模型评估和自适应数据分析时会系统比较这些方案。

</details>

---

## 延伸

- 统计推断：精确区间、检验的反演：卷零 0.3 节。
- KL 散度形式的切尔诺夫界：卷零 0.4 节。
- 测试集评估、分组划分与交叉验证：第 4 章。
- 同一份数据反复检验时的保证：第 5 章。
- 选择性分类中"不转人工部分"错误率的有限样本保证：第 7 章。
- 多臂老虎机与最优臂识别中的置信界：第 37、38 章。

## 文献

**教材**

- Stéphane Boucheron, Gábor Lugosi, Pascal Massart. *Concentration Inequalities: A Nonasymptotic Theory of Independence*. Oxford University Press, 2013. 集中不等式的标准参考书，切尔诺夫方法、次高斯、伯恩斯坦、有界差分都有系统处理。
- Roman Vershynin. *High-Dimensional Probability*. Cambridge University Press, 2018. 第 2 章讲独立变量和的集中，次高斯变量的处理清楚易读。
- Michael Mitzenmacher, Eli Upfal. *Probability and Computing*. Cambridge University Press, 2005（第 2 版 2017）. 乘法切尔诺夫界与鞅方法的入门讲法，例子来自算法分析。
- Devdatt Dubhashi, Alessandro Panconesi. *Concentration of Measure for the Analysis of Randomized Algorithms*. Cambridge University Press, 2009. 有界差分方法与鞅的大量应用。
- Shai Shalev-Shwartz, Shai Ben-David. *Understanding Machine Learning*. Cambridge University Press, 2014. 附录 B 汇总了学习理论常用的集中不等式。

**论文**

- Herman Chernoff. A Measure of Asymptotic Efficiency for Tests of a Hypothesis Based on the Sum of Observations. *Annals of Mathematical Statistics*, 23(4), 1952. 切尔诺夫方法。
- Wassily Hoeffding. Probability Inequalities for Sums of Bounded Random Variables. *Journal of the American Statistical Association*, 58(301), 1963. 霍夫丁不等式。
- George Bennett. Probability Inequalities for the Sum of Independent Random Variables. *Journal of the American Statistical Association*, 57(297), 1962. 伯恩斯坦不等式的改进形式（Bennett 不等式）。
- Kazuoki Azuma. Weighted Sums of Certain Dependent Random Variables. *Tohoku Mathematical Journal*, 19(3), 1967. 鞅差的集中不等式。
- Colin McDiarmid. On the Method of Bounded Differences. *Surveys in Combinatorics*, London Mathematical Society Lecture Note Series 141, 1989. 有界差分不等式。
- Andreas Maurer, Massimiliano Pontil. Empirical Bernstein Bounds and Sample Variance Penalization. *COLT*, 2009. 经验伯恩斯坦界。
- Jean-Yves Audibert, Rémi Munos, Csaba Szepesvári. Exploration–Exploitation Tradeoff Using Variance Estimates in Multi-Armed Bandits. *Theoretical Computer Science*, 410(19), 2009. 经验伯恩斯坦界在老虎机问题中的使用。
- Charles Clopper, Egon Pearson. The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial. *Biometrika*, 26(4), 1934. 精确二项区间。
