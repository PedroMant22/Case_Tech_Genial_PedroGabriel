Sistema de Validação de Suitability - Resolução CVM 30

Descrição:
Este sistema implementa um motor de validação de suitability baseado na Resolução CVM 30, que verifica se operações de investimento estão de acordo com o perfil de risco do cliente.

Estrutura de Dados Fictícios:

1. Perfil do Cliente:
   - Exemplo: {"perfil": "Moderado", "score_max_risco": 2.7}

2. Carteira Atual:
   - Lista de ativos, cada um com: ativo (nome), risco (0-10), valor_investido (R$)

3. Nova Ordem:
   - Ativo, risco, valor_ordem

Classe MotorSuitability:

Métodos:
- calcular_risco_carteira(carteira): Calcula o risco ponderado atual.
- calcular_risco_projetado(carteira_atual, nova_ordem): Projeta o risco incluindo a nova ordem.
- validar_desenquadramento(risco_projetado, score_max_risco): Retorna status (Aprovado, Alerta, Rejeitado) e limite de alerta.
- validar_ordem(perfil_cliente, carteira_atual, nova_ordem): Orquestra a validação e retorna resultado em JSON.

Regras de Validação:

- Aprovado: risco_projetado <= score_max_risco
- Alerta: score_max_risco < risco_projetado <= (score_max_risco * 1.10)
- Rejeitado: risco_projetado > (score_max_risco * 1.10)

Como Usar:

1. Execute o script Python: python motor_suitability.py

2. O script irá:
   - Calcular o risco atual da carteira.
   - Projetar o risco com a nova ordem.
   - Validar conforme as regras.
   - Exibir o resultado no console e salvar em 'resultado_validacao.json'.

Exemplo de Saída JSON:

{
  "status": "Aprovado",
  "risco_projetado": 2.45,
  "mensagem": "Ordem executada. Carteira em conformidade."
}

Arquivos Gerados:

- resultado_validacao.json: Contém o resultado da validação.

Considerações:

- Os dados fornecidos são fictícios.
- A escala de risco vai de 0 a 10.
- O sistema é baseado na Resolução CVM 30.

Próximos Passos Possíveis:

- Integração com base de dados real.
- Interface web para input de dados.
- Geração de relatórios detalhados.
