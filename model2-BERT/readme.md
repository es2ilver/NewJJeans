# 1.MakeTR_TSDataset

AI-hub에 있는 낚시성 기사 데이터중 연예 카테고리 추출후 필요(문장과 문장의 일관성 비교)에 맞는 데이터 구조에 맞게 전처리한 후 csv 파일로 저장.

# 2.MakeCheckpoint_klue_addtional

1.에서 저장한 csv로드 후 데이터프레임으로 변환.
각 데이터셋 임베딩후 model.fit으로 학습시킨후 체크포인트 저장.
테스트 정확도 확인.

# 3.KlueBert_Use_addtional

2.에서 체크포인트 로드후 실제 예측하고 싶은 데이터셋(연예기사)에 적용하여
연속된 문장사이의 predicted_classes(gold_label) 도출.
(gold_label = 0 : 두문장사이의 일관성 없음 ,
 gold_label = 1 : 두문장사이의 일관성 있음)

전체 predicted_classes 중 gold_label = 1 인것의 비율 구한후
기사의 일관성이 어느정도 일치하는지 도출.
