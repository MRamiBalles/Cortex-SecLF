import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { RoleProvider } from "@/src/context/RoleContext";
import RoleSwitcher from "@/src/components/RoleSwitcher";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Cortex-Sec Local Forge",
    description: "Autonomous Local Governance & Cybersecurity Forge",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" className="dark">
            <body className={inter.className}>
                <RoleProvider>
                    <div className="relative min-h-screen">
                        {children}
                        <RoleSwitcher />
                    </div>
                </RoleProvider>
            </body>
        </html>
    );
}
