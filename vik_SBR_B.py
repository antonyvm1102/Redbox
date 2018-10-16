Ts = 0.125
name = "nr_84_z.csv"
channel = 3

with open(name, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["file", "v_effmax", "v_max", "v_weighted_max"])
for fn in os.listdir():
    if fn.endswith(".txt"):
        if 1:
            print("file:", fn)
            df = pd.read_csv(fn, sep='  ', header=None)
            # Show original signal
            plt.plot(df[0], df[channel])
            plt.savefig("vik_original_signal_accel_{}".format(fn.replace("txt", "png")))
            plt.close()

            # Remove glitches in the signal
            df = df[df[channel] > -0.95]
            df.reset_index(inplace=True, drop=True)

            dt = df[0][1] - df[0][0]
            t = np.linspace(0, df.shape[0] * dt - dt, df.shape[0])

            plt.plot(t, df[channel])
            plt.savefig("vik_modified_signal_accel_{}".format(fn.replace("txt", "png")))
            plt.close()

            df[channel] = integrate_array(df[1] * 1000, t)
            vibrations = np.array(df[channel]) - df[channel].mean()

            print("compute fft")

            vibrations_fft = np.fft.fft(vibrations)
            T = t[1] - t[0]
            N = t.size

            f = np.linspace(0, 1 / T, N)

            weight = 1 / np.sqrt(1 + (5.6/ f)**2)
            vibrations_fft_w = weight * vibrations_fft
            vibrations_w = np.fft.ifft(vibrations_fft_w).real

            a = 8

            t = t[::a]
            vibrations_w = vibrations_w[::a]
            v_sqrd_w = vibrations_w**2

            v_eff = np.zeros(t.size)
            dt = t[1] - t[0]
            print("compute veff")

            for i in range(t.size - 1):
                g_xi = np.exp(-t[:i + 1][::-1] / Ts)
                v_eff[i] = np.sqrt(1 / Ts * np.trapz(g_xi * v_sqrd_w[:i + 1], dx=dt))

            idx = np.argmax(v_eff)
            plt.figure(figsize=(10,6))
            plt.plot(t, vibrations[::a], label="signal")
            plt.plot(t, vibrations_w, label="weighted_signal")
            plt.plot(t, v_eff, label="v_eff")
            plt.xlabel("t [s]")
            plt.ylabel("v [mm/s]")
            plt.title("velocity")
            plt.text(t[idx], v_eff[idx], "max v_eff: {}".format(round(v_eff[idx], 3)), color="r")
            plt.legend()
            plt.savefig("vik_{}".format(fn.replace("txt", "png")))
            plt.close("all")

            with open(name, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([fn, v_eff[idx], np.max(vibrations), np.max(vibrations_w)])