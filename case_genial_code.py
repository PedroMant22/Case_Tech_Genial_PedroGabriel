import json

# Dados de entrada ficticios 
perfil_cliente = {"perfil": "Moderado", "score_max_risco": 2.7}
carteira_atual = [
    {"ativo": "PETROBRAS", "risco": 6.2, "valor_investido": 50000},
    {"ativo": "EMBRAER", "risco": 4.0, "valor_investido": 4000},
    {"ativo": "BANCO DO BRASIL", "risco": 1.2, "valor_investido": 50000},
    {"ativo": "BRADESCO", "risco": 3.6, "valor_investido": 10000},
    {"ativo": "VALE", "risco": 2.2, "valor_investido": 50000},
    {"ativo": "AMBEV", "risco": 1.0, "valor_investido": 10000}
]
nova_ordem = {"ativo": "ITAU", "risco": 0.5, "valor_ordem": 5000}

class MotorSuitability:
    def calcular_risco_carteira(self, carteira):
        #Calcula o risco da carteira atual 
        if not carteira:
            return 0.0
        
        #Numerador: ∑ (Risco_i × ValorInvestido_i)
        risco_ponderado_total = sum(ativo['risco'] * ativo['valor_investido'] for ativo in carteira)
        
        #Denominador: ∑ ValorInvestido_i
        total_investido = sum(ativo['valor_investido'] for ativo in carteira)
        
        if total_investido == 0:
            return 0.0
        
        #Fórmula completa: RC = ∑ (Risco_i × ValorInvestido_i) / ∑ ValorInvestido_i
        risco_carteira = risco_ponderado_total / total_investido
        
        return risco_carteira

    def calcular_risco_projetado(self, carteira_atual, nova_ordem):
        #Calcula o risco projetado da compra 
        #Cria carteira projetada adicionando a nova ordem
        carteira_projetada = carteira_atual.copy()
        carteira_projetada.append({
            "ativo": nova_ordem["ativo"],
            "risco": nova_ordem["risco"],
            "valor_investido": nova_ordem["valor_ordem"]
        })
        
        #Recalcula o risco com a nova carteira
        return self.calcular_risco_carteira(carteira_projetada)

    def validar_desenquadramento(self, risco_projetado, score_max_risco):
        """
        C. Validação do Desenquadramento
        Compara o risco projetado com o score máximo + 10% para alerta
        Regra: Alerta se Risco_Projetado > Score_Max × 1.10
        """
        #Calcula o limite de alerta (10% acima do score máximo)
        limite_alerta = score_max_risco * 1.10
        
        #Aplica as regras de validação
        if risco_projetado <= score_max_risco:
            return "Aprovado", limite_alerta
        elif risco_projetado <= limite_alerta:
            return "Alerta", limite_alerta
        else:
            return "Rejeitado", limite_alerta

    def validar_ordem(self, perfil_cliente, carteira_atual, nova_ordem):
       #Execução da Validação 
        print("🔍 INICIANDO VALIDAÇÃO DE SUITABILITY - RESOLUÇÃO CVM 30")
        print("=" * 60)
        
        # A. Cálculo do Risco Atual da Carteira
        print("📊 A. CALCULANDO RISCO ATUAL DA CARTEIRA")
        risco_atual = self.calcular_risco_carteira(carteira_atual)
        
        #Mostra cálculo detalhado
        total_investido = sum(ativo['valor_investido'] for ativo in carteira_atual)
        risco_ponderado = sum(ativo['risco'] * ativo['valor_investido'] for ativo in carteira_atual)
        print(f"   ∑ (Risco_i × ValorInvestido_i) = {risco_ponderado:.2f}")
        print(f"   ∑ ValorInvestido_i = {total_investido:.2f}")
        print(f"   RC = {risco_ponderado:.2f} / {total_investido:.2f} = {risco_atual:.4f}")
        
        #B. Projeção do Risco Pós-Compra
        print("\n📈 B. PROJEÇÃO DO RISCO PÓS-COMPRA")
        risco_projetado = self.calcular_risco_projetado(carteira_atual, nova_ordem)
        
        # Mostra cálculo da projeção
        total_projetado = total_investido + nova_ordem['valor_ordem']
        risco_ponderado_projetado = risco_ponderado + (nova_ordem['risco'] * nova_ordem['valor_ordem'])
        print(f"   Nova ordem: {nova_ordem['ativo']} (Risco: {nova_ordem['risco']}, Valor: R$ {nova_ordem['valor_ordem']:.2f})")
        print(f"   ∑ (Risco_i × ValorInvestido_i) projetado = {risco_ponderado_projetado:.2f}")
        print(f"   ∑ ValorInvestido_i projetado = {total_projetado:.2f}")
        print(f"   RC Projetado = {risco_ponderado_projetado:.2f} / {total_projetado:.2f} = {risco_projetado:.4f}")
        
        #C. Validação do Desenquadramento
        print("\n⚖️  C. VALIDAÇÃO DO DESENQUADRAMENTO")
        score_max = perfil_cliente["score_max_risco"]
        status, limite_alerta = self.validar_desenquadramento(risco_projetado, score_max)
        
        print(f"   Score máximo do cliente: {score_max}")
        print(f"   Limite de alerta (+10%): {score_max} × 1.10 = {limite_alerta:.4f}")
        print(f"   Risco projetado: {risco_projetado:.4f}")
        print(f"   STATUS FINAL: {status}")
        
        #Gera saída no formato exato especificado
        return self._gerar_saida_json(status, risco_projetado, limite_alerta)

    def _gerar_saida_json(self, status, risco_projetado, limite_alerta):
        """Gera a saída JSON exatamente """
        if status == "Aprovado":
            return {
                "status": "Aprovado",
                "risco_projetado": round(risco_projetado, 2),
                "mensagem": "Ordem executada. Carteira em conformidade."
            }
            
        elif status == "Alerta":   #Alerta 
            return {
                "status": "Alerta",
                "risco_projetado": round(risco_projetado, 2),
                "mensagem": f"Atenção: O risco da carteira ultrapassará o limite de {limite_alerta:.2f}. É necessário termo de ciência."
            }
        else:  #Rejeitado
            return {
                "status": "Rejeitado", 
                "risco_projetado": round(risco_projetado, 2),
                "mensagem": "Risco excessivo. A operação viola a política de Suitability."
            }

# Exemplo de uso conforme especificado no case:
if __name__ == "__main__":
    motor = MotorSuitability()
    
    print("🎯 DADOS DE ENTRADA:")
    print(f"Perfil Cliente: {perfil_cliente}")
    print(f"Carteira com {len(carteira_atual)} ativos")
    print(f"Nova Ordem: {nova_ordem}")
    print()
    
    #Executar validação
    resultado = motor.validar_ordem(perfil_cliente, carteira_atual, nova_ordem)
    
    print("\n" + "🎯 RESULTADO DA VALIDAÇÃO (FORMATO JSON):")
    print("=" * 50)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    #Cálculo de verificação adicional
    print("\n" + "🧮 VERIFICAÇÃO DOS CÁLCULOS:")
    print("=" * 30)
    
    #Cálculo manual para confirmação
    total_atual = sum(ativo['valor_investido'] for ativo in carteira_atual)
    risco_ponderado_atual = sum(ativo['risco'] * ativo['valor_investido'] for ativo in carteira_atual)
    risco_atual_manual = risco_ponderado_atual / total_atual
    
    print(f"Risco Atual (verificação): {risco_atual_manual:.4f}")
    
    #Cálculo projetado manual
    total_projetado = total_atual + nova_ordem['valor_ordem']
    risco_ponderado_projetado = risco_ponderado_atual + (nova_ordem['risco'] * nova_ordem['valor_ordem'])
    risco_projetado_manual = risco_ponderado_projetado / total_projetado
    
    print(f"Risco Projetado (verificação): {risco_projetado_manual:.4f}")
    print(f"Limite de Alerta (2.5 × 1.1): {2.5 * 1.1:.2f}")