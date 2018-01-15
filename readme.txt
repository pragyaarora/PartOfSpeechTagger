1. Program File: Baseline.py
   Output File: mft_baseline.out

   python accuracy.py mft_baseline.out data/twitter_test_universal.txt

 2 and 3. bash eval.sh twitter

 4. For Penn Treebank data:
 	
 	bash eval.sh ptb

 	For NPS Chat data:
 	
 	bash eval.sh nps

 	For Twitter+NPS Chat data+Penn Treebank data:

 	bash eval.sh twitter_nps_ptb_train_universal

 5. NER without extra features
 	Comment line 23 in eval.sh and uncomment lines 25 and 26

 	bash eval.sh twitter

 	NER with extra features
 	Uncomment line 56 in Features.py

 	bash eval.sh twitter
	Output File : ner_ViterbiTagger.out.eval