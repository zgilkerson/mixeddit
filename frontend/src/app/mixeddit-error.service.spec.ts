import { TestBed, inject } from '@angular/core/testing';

import { MixedditErrorService } from './mixeddit-error.service';

describe('MixedditErrorService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MixedditErrorService]
    });
  });

  it('should be created', inject([MixedditErrorService], (service: MixedditErrorService) => {
    expect(service).toBeTruthy();
  }));
});
